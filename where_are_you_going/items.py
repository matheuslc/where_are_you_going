# -*- coding: utf-8 -*-

import scrapy

class Alumni(scrapy.Item):
    name = scrapy.Field()
    registry = scrapy.Field()
    semester = scrapy.Field()