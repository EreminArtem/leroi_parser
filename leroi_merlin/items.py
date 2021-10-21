# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose


def clear_price(value):
    try:
        value = int(value.replace(' ', ''))
    except:
        return value
    return value


class LeroiMerlinItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(clear_price), output_processor=TakeFirst())
    photos = scrapy.Field()
    _id = scrapy.Field()
