#!usr/bin/env python
# -*-coding:utf-8 -*-
__author__='WYY'
__date__='2017.03.17'

#爬虫实战小项目：pixabay图片搜索下载器
import re
import os
import requests
import urllib2
import time

class Spider():
    #初始化参数
    def __init__(self):
        self.keyword=raw_input(u'欢迎使用pixabay 图片搜索下载神器\n请输入搜索关键词(英文)：')
        self.siteURL='http://pixabay.com/zh/photos/?image_type=&cat=&min_width=&min_height=&q='+str(self.keyword)+'&order=popular'

    #获取详情页源码
    def getSource(self,url):
        result=requests.get(url).text.encode('utf-8')
        return result

    #获取图片页数
    def getPageNum(self):
        result=self.getSource(self.siteURL)
        pattern=re.compile('<input name="pagi.*?>.*?/ (.*?)&nbsp;.*?', re.S)
        items=re.search(pattern,result)
        if items.group(1)>=1:
            print u'\n这个主题共有图片', items.group(1), u'页'
        else:
            print u'\n哎呀，木有您想要的图呢。。。'
        return items.group(1)

    #匹配正则1
    def getItem1(self,url):
        result=self.getSource(url)
        pattern1=re.compile('<img srcset="https://cdn.pixabay.com/photo(.*?)-(.*?)__340.*?', re.S)
        items=re.findall(pattern1, result)
        return items

    #匹配正则2
    def getItem2(self,url):
        result=self.getSource(url)
        pattern2=re.compile('data-lazy-srcset="https://cdn.pixabay.com/photo(.*?)-(.*?)__340.*?', re.S)
        items=re.findall(pattern2,result)
        for item in items:
            print item
        return items

    #保存图片入文件
    def saveImage(self,detailURL,name):
        try:
            picture=urllib2.urlopen(detailURL)
            fileName=name+'.jpg'
            string='F:\Desktop\code\pixabay\%s\%s' % (self.path, fileName)
            E=os.path.exists(string)
            if not E:
                f=open(string, 'wb')
                f.write(picture.read())
                f.close()
            else:
                print u'图片已经存在，跳过！'
                return False
        except (urllib2.HTTPError,urllib2.URLError), e:
            print e.reason
            return None


    #创建目录
    def makeDir(self, path):
        self.path=path.strip()
        E=os.path.exists(os.path.join('F:\Desktop\code\pixabay', self.path))
        if not E:
            # 创建新目录,若想将内容保存至别的路径（非系统默认），需要更环境变量
            # 更改环境变量用os.chdir()
            os.makedirs(os.path.join('F:\Desktop\code\pixabay',self.path))
            os.chdir(os.path.join('F:\Desktop\code\pixabay',self.path))
            print u'成功创建名为', self.path, u'的文件夹'
            return self.path
        else:
            print u'名为', self.path, u'的文件夹已经存在...'
            return False

    #对一页的操作
    def saveOnePage(self,url):
        i=1
        items=self.getItem1(url)
        for item in items:
            detailURL='https://cdn.pixabay.com/photo'+str(item[0])+'-'+str(item[1])+ '_960_720.jpg'
            print u'\n', u'正在下载并保存图片', i, detailURL
            self.saveImage(detailURL, name='Num'+str(i))
            time.sleep(0.5)
            i+=1
        if i>16:
            items=self.getItem2(url)
            i=17
            for item in items:
                detailURL = 'https://cdn.pixabay.com/photo'+str(item[0])+'-'+str(item[1])+'_960_720.jpg'
                print u'\n', u'正在下载并保存图片', i, detailURL
                self.saveImage(detailURL,name='Num'+str(i))
                time.sleep(0.5)
                i += 1

    #对多页图片的操作
    def saveMorePage(self):
        numbers=self.getPageNum()
        Num=int(raw_input(u'一页共100张图，\n请输入要下载的页数(默认页数大于等于1）：'))
        Start=int(raw_input(u'请输入下载起始页数：'))
        if numbers>=1:
            for page in range(Start,Start+Num):
                if page==1:
                    print u'\n',u'正在获取第1页的内容......'
                    self.url1=self.siteURL
                    self.makeDir(path=self.keyword + 'page' + str(page))
                    self.saveOnePage(url=self.url1)
                else:
                    print u'\n',u'正在获取第',page, u'页的内容'
                    self.url2='https://pixabay.com/zh/photos/?orientation=&image_type=&cat=&colors=&q='+str(self.keyword)+'&order=popular&pagi='+str(page)
                    self.makeDir(path=self.keyword + 'page' + str(page))
                    self.saveOnePage(url=self.url2)

        else:
            return False

        print  u'\n',u'圆满成功!!!'

spider=Spider()
spider.saveMorePage()
