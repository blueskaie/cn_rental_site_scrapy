# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CityURLItem(scrapy.Item):

    cityname = scrapy.Field()
    cityname_pinyin = scrapy.Field()
    link = scrapy.Field()                            


class DistrictURLItem(CityURLItem):

    districname = scrapy.Field()
    districname_pinyin = scrapy.Field()
                         