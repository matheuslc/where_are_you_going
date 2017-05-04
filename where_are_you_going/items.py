# -*- coding: utf-8 -*-

import scrapy

class Alumni(scrapy.Item):
  _id = scrapy.Field()
  name = scrapy.Field()
  registry = scrapy.Field()
  semester = scrapy.Field()
  situation = scrapy.Field()
  course = scrapy.Field()
  curriculum = scrapy.Field()
  semester = scrapy.Field()