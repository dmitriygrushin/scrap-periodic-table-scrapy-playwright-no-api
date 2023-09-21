# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags


class PeriodicElementItem(scrapy.Item):
    symbol = scrapy.Field(
        # processors are used to process the data before it is stored in the item,
        #   and after it is extracted from the web page, respectively.
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    name = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
    atomic_number = scrapy.Field(
        # when working with a site that doesn't have consistent data it's better NOT to make it an (int) right away,
        #   but instead (try to cast to an int), if it fails handle the exception. In this case the data is consistent
        #   so, using input_processor=MapCompose(..., int) is okay. i.e. You may get a (-) where an in an (int) column
        input_processor=MapCompose(remove_tags, str.strip, int),
        output_processor=TakeFirst()
    )
    atomic_mass = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip, float),
        output_processor=TakeFirst()
    )
    chemical_group = scrapy.Field(
        input_processor=MapCompose(remove_tags, str.strip),
        output_processor=TakeFirst()
    )
