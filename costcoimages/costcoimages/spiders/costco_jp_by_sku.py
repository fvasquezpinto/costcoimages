import csv
import logging
import re
from datetime import datetime

import w3lib
import scrapy

from costcoimages.items import CostcoimagesItem as Item


logger = logging.getLogger('CostcoImages')

class CostcoSpider(scrapy.Spider):

    name = "CostcoJPbySKU"
    base_url = "https://www.costco.co.jp"
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
    file.write("sku;img_url;name;features;description\n")
    file.close()

    error_file = open(f"costcoimages/spiders/output/error_file_{file_timestamp}.csv", "w", encoding='utf8')
    error_file.write("product_url\n")
    error_file.close()

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

    def start_requests(self):

        for sku in self.skus:
            url = f"{self.base_url}/p/{sku}"
            yield scrapy.Request(url=url, callback=self.parse_product)

    def parse_product(self, response):
        img_url = response.xpath(
            "//div[@class='page-content container main-wrapper'] //picture /source[@type='image/webp'] /@srcset"
        ).get()

        product_url = response.url
        sku = product_url.split("/")[-1]

        name = response.xpath(
            "//h1[@class='product-name'] /text()"
        ).get()

        if not name:
            return

        text_features = []
        features = response.xpath(
            "//div[@class='product-information-text'] /ul /li"
        )
        for feature in features:
            text = feature.xpath("./p /text()").get()
            if not text:
                text = feature.xpath("./text()").get()
            #if text:
            text_features.append(text.strip())

        text_descriptions = []
        descriptions = response.xpath(
            "//div[@class='product-details-wrapper'] /div /p"
        )
        for description in descriptions:
            text = description.xpath("./text()").get()
            text_descriptions.append(text.strip())
        
            item = Item()
            item["sku"] = sku
            item["img_url"] = "".join([self.base_url, img_url])
            item["name"] = name
            try:
                item["description"] = "    <br>    ".join(text_descriptions)
            except TypeError:
                item["description"] = None
            try:
                item["features"] = "    <br>    ".join(text_features)
            except TypeError:
                item["features"] = None

        try:
            yield item
        except UnboundLocalError:
            error_file = open(f"costcoimages/spiders/output/error_file_{self.file_timestamp}.csv", "w", encoding='utf8')
            error_file.write(f"{str(response.url)}\n")
            error_file.close()

        logger.info(f"Data saved for product with sku {sku}.")
