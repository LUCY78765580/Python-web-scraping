# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from XiaoHua import settings
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class XiaohuaPipeline(ImagesPipeline):
    def get_media_requests(self, item,info):
        yield scrapy.Request(item['detailURL'])

    def item_completed(self,results,item,info):
        path=[x['path'] for ok,x in results if ok]
        if not path:
            raise DropItem('Item contains no images')
        print u'正在保存图片：', item['detailURL']
        print u'主题', item['title']
        return item
