from datetime import datetime


class CostcoimagesPipeline:
    def process_item(self, item, spider):
        item_sku = item["sku"]
        item_img_url = item["img_url"]
        item_name = item["name"]
        item_features = item["features"]
        item_description = item["description"]
        text = ";".join([item_sku, item_img_url, item_name, item_features, item_description])
        text = "".join([text, "\n"])

        filename = "_".join(
        	["costcoimages/spiders/output/costco_jp_images", spider.file_timestamp]
        )
        filename = ".".join([filename, "csv"])
        with open(filename, 'a', encoding='utf8') as f:
            f.write(text)
