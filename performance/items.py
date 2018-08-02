# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PerformanceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # link 字段用于保存已经爬取过的页面，检查它可以不再重复爬取
    link = scrapy.Field()

    # name, date, place, price, contact, producer 组成演出的元组信息
    name = scrapy.Field()
    date = scrapy.Field()
    place = scrapy.Field()
    price = scrapy.Field()
    contact = scrapy.Field()
    producer = scrapy.Field()

    pass
