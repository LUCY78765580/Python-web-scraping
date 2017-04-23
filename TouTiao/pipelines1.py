# -*- coding: utf-8 -*-
import xlwt
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class ToutiaoPipeline(object):
    def __init__(self):
        self.book=xlwt.Workbook()
        self.sheet=self.book.add_sheet('sheet', cell_overwrite_ok=True)
        head=[u'名字', u'点赞', u'回复', u'评论']
        i=0
        for h in head:
            self.sheet.write(0, i, h)
            i += 1
    def process_item(self,item,spider):
        self.sheet.write(item['Num'],0,item['name'])
        self.sheet.write(item['Num'],1,item['like'])
        self.sheet.write(item['Num'],2,item['reply'])
        self.sheet.write(item['Num'],3,item['text'])
        self.book.save('TouTiao.xls')
