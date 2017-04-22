#!usr/bin/env python
# -*-coding:utf-8 -*-
__author__='WYY'
__date__='2017.03.26'

#实战小项目：爬取教务网成绩并存入excel
import requests
import xlwt
from bs4 import BeautifulSoup

#模拟登录
formData={'zjh':'2014141431216','mm':'xxxxxx'}
s=requests.Session()
Post=s.post(url='http://zhjw.scu.edu.cn/loginAction.do',data=formData)
print Post.status_code
#获取基本信息
detailURL='http://zhjw.scu.edu.cn/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2016-2017%D1%A7%C4%EA%C7%EF(%C1%BD%D1%A7%C6%DA)'
html=s.get(url=detailURL)
main=html.content.decode('gbk')
soup=BeautifulSoup(main,'lxml')
content=soup.find_all('td',align="center")
#将信息放入一个list中,创建new_list(方便后续存入excel)
data_list=[]
for data in content:
    data_list.append(data.text.strip())
new_list=[data_list[i:i+7] for i in range(0,len(data_list),7)]
#数据存入excel表格
book=xlwt.Workbook()
sheet1=book.add_sheet('sheet1',cell_overwrite_ok=True)
heads=[u'课程号',u'课序号',u'课程名',u'英文课程名',u'学分',u'课程属性',u'成绩']
print u'\n准备将数据存入表格...'
ii=0
for head in heads:
    sheet1.write(0,ii,head)
    ii+=1
i=1
for list in new_list:
    j=0
    for data in list:
        sheet1.write(i,j,data)
        j+=1
    i+=1
book.save('JiaoWuChengJi.xls')
print u'\n录入成功！'
