# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CostcoimagesItem(scrapy.Item):
    sku = scrapy.Field()
    img_url = scrapy.Field()
    product_url = scrapy.Field()
