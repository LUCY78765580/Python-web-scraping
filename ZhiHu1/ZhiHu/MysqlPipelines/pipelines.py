# -*- coding: utf-8 -*-
from ZhiHu.items import ZhihuItem
from ZhiHu.spiders.zhihu import Myspider
from Mysql import MySql
import mysql.connector

class ZhihuPipeline(object):
    def process_item(self,item,spider):
        if isinstance(item,ZhihuItem):
            try:
                MySql.insert_db(item)
                Myspider.Save_Num+=1  #每次插入数据成功加1
                print u'成功！'
            except mysql.connector.IntegrityError as e:
                print 'mysql.connector.IntegrityError'
                print u'主键重复，不存入'


