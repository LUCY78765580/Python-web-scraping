# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ToutiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Num=scrapy.Field()
    text=scrapy.Field()  #评论内容
    name=scrapy.Field()  #评论者名字
    like=scrapy.Field()  #点赞数
    reply=scrapy.Field()  #回复数
