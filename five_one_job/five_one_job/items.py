# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FiveOneJobItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jobtitle = scrapy.Field()
    link = scrapy.Field()
    company = scrapy.Field()
    location = scrapy.Field()
    money = scrapy.Field()
    update_time = scrapy.Field()
    position_zhize = scrapy.Field()
    position_company = scrapy.Field()
