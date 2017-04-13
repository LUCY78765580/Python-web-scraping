# -*- coding: utf-8 -*-
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class XiaohuaPipeline(object):
    def process_item(self, item, spider):
        detailURL=item['detailURL']
        path=item['path']
        fileName=item['fileName']

        image=requests.get(detailURL)
        f=open(path,'wb')
        f.write(image.content)
        f.close()
        print u'正在保存图片：',detailURL
        print u'图片路径：',path
        print u'文件：',fileName
        return item
