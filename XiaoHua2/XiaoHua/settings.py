# -*- coding: utf-8 -*-
# Scrapy settings for XiaoHua project
BOT_NAME = 'XiaoHua'
SPIDER_MODULES = ['XiaoHua.spiders']
NEWSPIDER_MODULE = 'XiaoHua.spiders'

#是否遵守机器人规则
ROBOTSTXT_OBEY = False
#一次可以requests请求的最大次数，默认16，
CONCURRENT_REQUESTS=16
#下载延迟设置为1s
DOWNLOAD_DELAY=1
#禁用Cookies
COOKIES_ENABLED = False
#设置headers
DEFAULT_REQUEST_HEADERS = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}

#管道设置
ITEM_PIPELINES = {'XiaoHua.pipelines.XiaohuaPipeline': 1}
IMAGES_STORE=r'F:\\Desktop\code\info\XiaoHua2'

#IMAGES_THUMBS用于生成大小不同的缩略图
#以字典形式表示，键为文件名，值为图片尺寸
IMAGES_THUMBS={
    'small': (50, 50),
    'big': (200, 200),}

#以下两个设置可以过滤尺寸小于100的图片
IMAGES_MIN_HEIGHT=100
IMAGES_MIN_WIDTH=100

#IMAGES_EXPIRES用于设置
#90天的失效期限，避免管道重复下载最近已经下载过的
IMAGES_EXPIRES=90
