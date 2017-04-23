# -*- coding:utf-8 -*-
import scrapy
from scrapy.http import Request
from TouTiao.items import ToutiaoItem
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Myspider(scrapy.Spider):
    name='TouTiao'
    allowed_domains=['snssdk.com']
    Num=1
    def start_requests(self):
        #这里具体抓手机的Api地址（与型号有关）
        #最精简的URL（可以试出来）
        urls=['http://lf.snssdk.com/article/v2/tab_comments/?group_id=6389542758708675073&offset='+str(i)for i in range(0,1200)]
        for url in urls:
            yield Request(url,callback=self.parse)

    def parse(self,response):
        #解析json格式数据
        data=json.loads(response.text)['data']
        for i in data:
            # 每一项评论创建一个Item实例
            item = ToutiaoItem()
            comment=i['comment']
            item['Num']=self.Num
            item['text']=comment['text']
            item['name']=comment['user_name']
            item['like']=comment['digg_count']
            item['reply']=comment['reply_count']
            #打印测试结果
            print u'\n'
            print u'序号：',item['Num']
            print u'评论：',item['text']
            print u'名字：',item['name']
            print u'点赞：',item['like']
            print u'回复：',item['reply']
            #Num设置为全局变量，方便查看进度
            self.Num+=1
            return item



