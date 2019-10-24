#!usr/bin/env python
# -*-coding:utf-8 -*-
__author__='WYY'
__date__='2017.03.22'

#实战小项目：爬取pexels网站获取高清原图（做成图片下载器）
import re
import os
import requests
import random
import time

class Spider():
    def __init__(self):
        self.keyword=raw_input(u'欢迎使用 pexels 图片搜索下载神器\n请输入搜索关键词(英文)：')
        self.siteURL='https://www.pexels.com/search/'+str(self.keyword)+'/'

    def getSource(self,url):
        result=requests.get(url).text.encode('utf-8')
        return result

    #获取图片页数
    def getPageNum(self):
        result=self.getSource(url=self.siteURL)
        pattern=re.compile('<span class="gap".*?<a href="/search/.*?>(.*?)</a> <a href="/search/.*?>(.*?)</a> <a class="next_page" rel="next"', re.S)
        items=re.search(pattern,result)
        if items.group(2)>=1:
            print u'\n这个主题共有图片', items.group(2), u'页'
        else:
            print u'\n哎呀，木有您想要的图呢。。。'
        return items.group(2)

    #获取链接部分
    def getPartLink(self,url):
        result=self.getSource(url)
        pattern1=re.compile(r'<img.*?data-pin-media="https://images.pexels.com/photos/(.*?)/(.*?)?w=800.*?>', re.S)
        items=re.findall(pattern1, result)
        return items

    #保存图片入文件
    def saveImage(self,detailURL,name):
        fileName=name
        string='F:\Desktop\code\pexels\%s\%s' % (self.path, fileName)
        E=os.path.exists(string)
        if not E:
            try:
                user_agents=['Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0',
                           'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0',
                           'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533+ \(KHTML, like Gecko) Element Browser 5.0',
                           'IBM WebExplorer /v0.94', 'Galaxy/1.0 [en] (Mac OS X 10.5.6; U; en)',
                           'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
                           'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
                           'Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) \Version/6.0 Mobile/10A5355d Safari/8536.25',
                           'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) \Chrome/28.0.1468.0 Safari/537.36',
                           'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)']
                index=random.randint(0, 9)
                user_agent=user_agents[index]
                headers={'User_agent':user_agent}
                picture=requests.get(detailURL,headers)
                f=open(string, 'wb')
                f.write(picture.content)
                f.close()
            except requests.exceptions.ConnectionError:
                print 'Download error:requests.exceptions.ConnectionError'
                return None
        else:
            print u'图片已经存在，跳过！'
            return False

    #创建目录
    def makeDir(self, path):
        self.path=path.strip()
        E=os.path.exists(os.path.join('F:\Desktop\code\pexels', self.path))
        if not E:
            os.makedirs(os.path.join('F:\Desktop\code\pexels',self.path))
            os.chdir(os.path.join('F:\Desktop\code\pexels',self.path))
            print u'成功创建名为', self.path, u'的文件夹'
            return self.path
        else:
            print u'名为', self.path, u'的文件夹已经存在...'
            return False

    #对一页的操作
    def saveOnePage(self,oneURL):
        items=self.getPartLink(oneURL)
        i=1
        for item in items:
            #记得去掉后面的'?'
            detailURL='https://static.pexels.com/photos/'+item[0]+'/'+item[1][:-1]
            print u'\n', u'正在下载并保存图片',i
            self.saveImage(detailURL,name=item[1][:-1])
            time.sleep(0.5)
            i+=1

    #对多页的操作
    def saveMorePage(self):
        Numbers=self.getPageNum()
        Num=int(raw_input(u'一页共15张图，\n请输入要下载的页数(默认页数大于等于1）：'))
        Start=int(raw_input(u'请输入下载起始页数：'))
        if Numbers>=1:
            for page in range(Start,Start+Num):
                print u'\n',u'正在获取第',page, u'页的内容'
                self.url='https://www.pexels.com/search/'+str(self.keyword)+'/?page='+str(page)
                self.makeDir(path=self.keyword+'Page'+str(page))
                self.saveOnePage(oneURL=self.url)
                time.sleep(5)
        else:
            return False

        print  u'\n',u'圆满成功!!!'

spider=Spider()
spider.saveMorePage()
