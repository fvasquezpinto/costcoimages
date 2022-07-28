import csv
import logging
import re
from datetime import datetime

import w3lib
import scrapy

from costcoimages.items import CostcoimagesItem as Item


logger = logging.getLogger('CostcoImages')

class CostcoSiteMapSpider(scrapy.spiders.XMLFeedSpider):

    name = "CostcoJP"
    base_url = "https://www.costco.co.jp"
    allowed_domains = ["costco.co.jp"]
    start_urls = ["https://www.costco.co.jp/sitemap_japan_product.xml"]
    itertag = 'url'
    file_timestamp = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")

    skus = []

    # Input file
    with open(
        "costcoimages/spiders/costco_images_input_skus.csv", "r"
    ) as input_file:
        reader = csv.DictReader(input_file, delimiter=";")
        for row in reader:
            skus.append(row["sku"])

    # Creates file when scraper runs
    filename = "_".join(
        ["costcoimages/spiders/output/costco_jp_images", file_timestamp]
    )
    filename = ".".join([filename, "txt"])
    file = open(filename, "w", encoding='utf8')
    file.write("sku;img_url;product_url\n")
    file.close()

    custom_settings = {
        "ITEM_PIPELINES": {"costcoimages.pipelines.CostcoimagesPipeline": 0},
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": None,
        },
        "DOWNLOAD_DELAY": 1,
        "AUTOTHROTTLE_ENABLED": True,
        "AUTOTHROTTLE_START_DELAY": 1,
        "AUTOTHROTTLE_TARGET_CONCURRENCY": 4
    }        

    def parse_node(self, response, node):

        data = None
        for node_text in node.xpath("//*").getall():
            if "<loc>" in node_text:
                data = node_text

        product_url = re.search("<loc>(.*?)</loc>", data).group(0)
        product_url = w3lib.html.remove_tags(product_url)
        sku = product_url.split("/")[-1]
        try:
            img_url = re.search("<image:loc>(.*?)</image:loc>", data).group(0)
        except AttributeError:
            if sku in self.skus:
                # Go to search the image in the page of the product
                yield response.follow(
                    url=product_url,
                    callback=self.parse_product
                )
            return

        img_url = w3lib.html.remove_tags(img_url)

        if sku in self.skus:

            item = Item()
            item["sku"] = sku
            item["img_url"] = img_url
            item["product_url"] = product_url

            yield item

            logger.info(f"Data saved for product with sku {sku}.")

    def parse_product(self, response):
        img_url = response.xpath(
            "//div[@class='page-content container main-wrapper'] //picture /source[@type='image/webp'] /@srcset"
        ).get()
        product_url = response.url
        sku = product_url.split("/")[-1]

        item = Item()
        item["sku"] = sku
        item["img_url"] = "".join([self.base_url, img_url])
        item["product_url"] = product_url

        yield item

        logger.info(f"Data saved for product with sku {sku}.")

