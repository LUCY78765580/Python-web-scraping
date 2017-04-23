# -*- coding: utf-8 -*-

BOT_NAME = 'TouTiao'
SPIDER_MODULES = ['TouTiao.spiders']
NEWSPIDER_MODULE = 'TouTiao.spiders'

ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 2
COOKIES_ENABLED = False

DEFAULT_REQUEST_HEADERS = {
    'Accept-Encoding':'gzip',
    'Connection':'keep-alive',
    'User_agent':'Dalvik/2.1.0 (Linux; U; Android 5.1.1; vivo V3Max A Build/LMY47V)'
}

ITEM_PIPELINES = {'TouTiao.pipelines.ToutiaoPipeline': 300}
