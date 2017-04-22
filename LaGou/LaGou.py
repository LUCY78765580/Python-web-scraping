#!usr/bin/env python
# -*-coding:utf-8 -*-
__author__='WYY'
__date__='2017.03.29'

#实战小项目：爬取拉钩网并作小型数据分析
import requests
import json
import xlwt
import time
import random

class Spider():
    def __init__(self):
        self.keyword=raw_input(u'请输入职位：')

    #获取数据
    def getData(self,url):
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
        #cookie要自己抓
        headers={'User_agent':user_agent,
                 'cookie':'your cookies'}
        html=requests.get(url,headers=headers)
        data=json.loads(html.text)
        return data

    #获取职位信息并存入列表
    def getPosition(self,url):
        data=self.getData(url)
        position=data['content']['positionResult']['result']
        po_list=[]
        if position is not None:
            for i in position:
                main=[]
                main.append(i['companyFullName'])
                main.append(i['financeStage'])
                main.append(i['positionName'])
                main.append(i['positionLables'])
                main.append(i['salary'])
                main.append(i['city'])
                main.append(i['education'])
                main.append(i['workYear'])
                main.append(i['jobNature'])
                main.append(i['createTime'])
                po_list.append(main)
        return po_list

    #获取数据,存入一个大的list
    def saveDetail(self):
        self.New=int(raw_input(u'请输入要爬取的页数:'))
        self.time=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print u'\n本地时间：',self.time
        print u'\n开始采集数据...'
        container=[]
        for page in range(1,self.New+1):
            self.url='https://www.lagou.com/jobs/positionAjax.json?px=new&first=true&pn='+str(page)+'&kd='+str(self.keyword)
            po_list=self.getPosition(self.url)
            time.sleep(3)
            print u'第',page,u'项完毕'
            container=container+po_list
        return container

    #将数据存入excel
    def saveAll(self):
        book=xlwt.Workbook()
        sheet =book.add_sheet(str(self.keyword), cell_overwrite_ok=True)
        container=self.saveDetail()
        print u'\n采集完毕'
        print u'\n准备将数据存入表格...'
        heads=[u'公司全名', u'融资状况', u'工作名称', u'标签', u'薪酬', u'城市', u'学历要求',u'经验要求',u'工作类型',u'数据创建时间']
        ii=0
        for head in heads:
            sheet.write(0,ii,head)
            ii+=1
        i=1
        for list in container:
            j=0
            for one in list:
                sheet.write(i, j, one)
                j+=1
            i+=1
        book.save(str(self.keyword)+'.xls')
        print u'\n录入成功！'

spider=Spider()
spider.saveAll()

