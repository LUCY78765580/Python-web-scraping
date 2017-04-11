# !usr/bin/env python
#  -*- coding: utf-8 -*-
__date__='2017.04.07'
__author__='WYY'

import jieba.analyse
f=open(r'F:\Desktop\DouBan.txt','r')
content=f.read()

try:
    jieba.analyse.set_stop_words(r'F:\Desktop\TingYong.txt')
    tags=jieba.analyse.extract_tags(content,topK=150, withWeight=True)
    for item in tags:
        print item[0]+'\t'+str(int(item[1]*10000))
finally:
    f.close()