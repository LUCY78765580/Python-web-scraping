#!usr/bin/env python
# -*- coding: utf-8 -*-
__date__='2017.04.06'
__author__='WYY'

#实战小项目：爬取豆瓣有关张国荣的日记（并作数据分析)
import requests
import json
import re
from bs4 import BeautifulSoup
import itertools
import time
import xlwt
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Tool():
    def replace(self,x):
        x=re.sub(re.compile('<br>|</br>|&nbsp;|<p>|</p>|<td>|</td>|<tr>|</tr>|</a>|<table>|</table>'), "", x)
        x=re.sub(re.compile('<div.*?>|<img.*?>|<a.*?>|<td.*?>'), "", x)
        return x.strip()

class Spider():
    def __init__(self):
        self.tool=Tool()

    def get_source(self,url):
        cookies='bid=6xgbcS6Pqds; ll="118318"; viewed="3112503"; gr_user_id=660f3409-0b65-4195-9d2f-a3c71573b40f; ct=y; ps=y; _ga=GA1.2.325764598.1467804810; _vwo_uuid_v2=112D0E7472DB37089F4E96B7F4E5913D|faf50f21ff006f877c92e097c4f2819c; ap=1; push_noty_num=0; push_doumail_num=0; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1491576344%2C%22http%3A%2F%2Fwww.so.com%2Flink%3Furl%3Dhttp%253A%252F%252Fwww.douban.com%252F%26q%3D%25E8%25B1%2586%25E7%2593%25A3%26ts%3D1491459621%26t%3Df67ffeb4cd66c531150a172c69796e0%26src%3Dhaosou%22%5D; __utmt=1; _pk_id.100001.8cb4=41799262efd0b923.1467804804.35.1491576361.1491567557.; _pk_ses.100001.8cb4=*; __utma=30149280.325764598.1467804810.1491566154.1491576346.34; __utmb=30149280.3.10.1491576346; __utmc=30149280; __utmz=30149280.1491469694.24.15.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.12683; dbcl2="126831173:APSgA3NPab8"'
        headers={'User_Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36','Cookie':cookies}
        s=requests.Session()
        response=s.get(url,headers=headers)
        requests.adapters.DEFAULT_RETRIES=5
        return response

    def get_main(self):
        mains=[]
        print u'\n',u'正在解析页面...'
        for i in range(1020,2001,20):
            response=self.get_source(url='https://www.douban.com/j/search?q=张国荣+&start='+str(i)+'&cat=1015')
            main=json.loads(response.text)['items']
            mains.append(main)
        print u'\n', u'解析页面成功！'
        return mains

    def get_link(self):
        n=1
        links=[]
        mains=self.get_main()
        print u'正在获取链接...'
        for main in mains:
            try:
                for j in itertools.count(0):
                    soup=BeautifulSoup(main[j],'lxml').find('h3')
                    pattern=re.compile(r'<a href=.*?sid:(.*?)>(.*?)</a>', re.S)
                    items=re.findall(pattern, str(soup))
                    for item in items:
                        id=item[0][0:-3].strip()
                        link='https://www.douban.com/note/'+str(id)+'/'
                        print link
                        links.append(link)
                        time.sleep(0.2)
                        n+=1
            except IndexError:
                continue
        print u'\n', u'成功将所有链接存入list!',u'\n',u'一共',n-1,u'项'
        return links

    def get_detail(self):
        links=self.get_link()
        container=[]
        print u'\n',u'正在获取详细信息...'
        n=1
        for link in links:
            html=self.get_source(link).text
            data=[]
            patternNum=re.compile(r'class="fav-num"',re.S)
            Num=re.search(patternNum,html)
            if Num:
                pattern=re.compile(r'<h1>(.*?)</h1>.*?<a href=.*?class="note-author">(.*?)</a>.*?<span class="pub-date">(.*?)</span>.*?<div class="note" id="link-report">(.*?)</div>.*?<span class="fav-num".*?>(.*?)</span>',re.S)
                items=re.findall(pattern,html)
                for item in items:
                    data.append(item[0])
                    data.append(link)
                    data.append(item[1])
                    data.append(item[2])
                    data.append(item[4])
                    data.append(self.tool.replace(item[3]))
            else:
                pattern=re.compile(r'<h1>(.*?)</h1>.*?<a href=.*?class="note-author">(.*?)</a>.*?<span class="pub-date">(.*?)</span>.*?<div class="note" id="link-report">(.*?)</div>',re.S)
                items=re.findall(pattern, html)
                for item in items:
                    data.append(item[0])
                    data.append(link)
                    data.append(item[1])
                    data.append(item[2])
                    data.append('0')
                    data.append(self.tool.replace(item[3]))
            container.append(data)
            print u'第', n, u'项结束'
            time.sleep(0.5)
            n+=1
        print u'\n',u'成功将所有信息写入list!'
        return container

    def save_detail(self):
        book=xlwt.Workbook()
        sheet=book.add_sheet('sheet1',cell_overwrite_ok=True)
        heads=[u'标题',u'链接',u'作者',u'发布时间',u'喜欢']
        ii=0
        for head in heads:
            sheet.write(0,ii,head)
            ii+=1

        container=self.get_detail()
        f=open(r'F:\Desktop\DouBan2.txt','w')
        i=1
        for list in container:
            f.writelines(list[5].encode('utf-8'))
            list.remove(list[5])
            j=0
            for data in list:
                sheet.write(i,j,data)
                j+=1
            i+=1
        f.close()
        print u'\n\n',u'录入txt成功！'
        book.save('DouBan2.xls')
        print u'\n\n',u'录入Excel成功!'

spider=Spider()
spider.save_detail()
