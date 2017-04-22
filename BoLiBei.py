#!usr/bin/env python
# -*-coding:utf-8 -*-
__author__='WYY'
__date__='2017.03.24'

#实战小项目：爬取SCU-info玻璃杯事件，提取热门100条神回复
import requests
import json
import re
import time

class Spider():
    #初始化，记录采集时间
    def __init__(self):
        self.time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print u'\n',u'开始采集数据',u'\n本地时间：',self.time

    #获取data
    def getData(self,url):
        html=requests.get(url).text
        requests.adapters.DEFAULT_RETRIES=5
        result=json.loads(html)
        data=result['data']
        return data

    #获取最新的评论id
    def getNew(self):
        data=self.getData(url='http://www.scuinfo.com/api/posts?pageSize=15')
        New=data[0]['id']
        return New

    #提取data中有效数据，写入一个dict，多项写入一个list
    def getDetail(self):
        New=self.getNew()
        container=[]
        i=1
        for id in range(131599,New+1):
            content={}
            self.url='http://www.scuinfo.com/api/post?id='+str(id)
            data=self.getData(url=self.url)
            if not isinstance(data,list):
                body=data.values()[7]
                likeCount=data.values()[6]
                comment=data.values()[0]
                #关键词分别为“玻璃”、“杯”、“摔”、“观光”
                pattern=re.compile(u'\u73bb\u7483|\u676f|\u6454|\u89c2\u5149',re.S)
                items=re.search(pattern,body)
                if items:
                    content['body']=body
                    content['like']=likeCount
                    content['comment']=comment
                    print u'\n', i, u'\n', u'发言：', body, u'\n', u'点赞:', likeCount, u'', u'评论：', comment
                    time.sleep(0.01)
                    i += 1
                    container.append(content)
            else:
                print 'None'
        print u'\n\n', u'至', self.time, u'为止，info上关于玻璃杯事件，共有评论',i-1, u'条'
        return container

    #获取评论总数
    #依据点赞数由大到小将评论排列，获取前100条热门评论
    def getSort(self):
        container=self.getDetail()
        print u'\n',u'将人气最高的前100条打印如下：'
        container.sort(key=lambda k:k.get('comment',0))
        container.sort(key=lambda k:k.get('like',0),reverse=True)
        for index,r in enumerate(container):
            print u'\n\n序号：',index+1, u'\n发言：',r['body'],u'\n点赞：' ,r['like'],u'评论',r['comment']
spider=Spider()
spider.getSort()
