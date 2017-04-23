# -*- coding: utf-8 -*-
#导入settings中各种参数
from scrapy.conf import settings
import pymongo


class MongoPipeline(object):
    def __init__(self):
        #pymongo.MongoClient连接到数据库
        connection=pymongo.MongoClient(settings['MONGODB_HOST'],settings['MONGODB_PORT'])
        # 创建数据库'db1'
        db=connection[settings['MONGODB_NAME']]
        # 连接到数据集'toutiao'，类型为dict
        self.post=db[settings['MONGODB_DOCNAME']]

    def process_item(self,item,spider):
        #插入数据到数据库
        self.post.update({'text':item['text']},{'$set':dict(item)},upsert=True)
        print u'插入成功!'
        return item





