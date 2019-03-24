# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    plot = scrapy.Field()
    street = scrapy.Field()
    district = scrapy.Field()
    time = scrapy.Field()
    money = scrapy.Field()
    typ = scrapy.Field()
    area = scrapy.Field()
    orientation = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    subway = scrapy.Field()

