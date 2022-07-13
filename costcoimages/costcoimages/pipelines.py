from datetime import datetime


class CostcoimagesPipeline:
    def process_item(self, item, spider):
        item_sku = item["sku"]
        item_img_url = item["img_url"]
        item_product_url = item["product_url"]
        text = ";".join([item_sku, item_img_url, item_product_url])
        text = "".join([text, "\n"])

        filename = "_".join(
        	["costcoimages/spiders/output/costco_jp_images", spider.file_timestamp]
        )
        filename = ".".join([filename, "txt"])
        with open(filename, 'a', encoding='utf8') as f:
            f.write(text)
