# -*- coding: utf-8 -*-
# Scrapy settings for TouTiao project

BOT_NAME = 'TouTiao'
SPIDER_MODULES = ['TouTiao.spiders']
NEWSPIDER_MODULE = 'TouTiao.spiders'

ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False

CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1

#设置headers，UA改为手机的配置
DEFAULT_REQUEST_HEADERS = {
    'Accept-Encoding':'gzip',
    'Connection':'keep-alive',
    'User_agent':'Dalvik/2.1.0 (Linux; U; Android 5.1.1; vivo V3Max A Build/LMY47V)'}

#记得将ITEM_PIPELINES改为MongoPipeline
ITEM_PIPELINES = {'TouTiao.pipelines.MongoPipeline': 300}

#数据库的一些参数
MONGODB_HOST='127.0.0.1'
MONGODB_PORT=27017
MONGODB_NAME='db1'
MONGODB_DOCNAME='toutiao'