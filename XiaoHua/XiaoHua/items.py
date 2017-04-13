# -*- coding: utf-8 -*-

# Define here the models for your scraped items
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy

class XiaohuaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    siteURL=scrapy.Field()
    pageURL=scrapy.Field()
    detailURL=scrapy.Field()
    title=scrapy.Field()
    fileName=scrapy.Field()
    path=scrapy.Field()

    
