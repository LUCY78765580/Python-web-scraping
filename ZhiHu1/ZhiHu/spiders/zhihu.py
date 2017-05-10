# -*- coding:utf-8 -*-
import scrapy
from scrapy.http import Request
from ZhiHu.items import ZhihuItem
from ZhiHu.MysqlPipelines.Mysql import NumberCheck
from scrapy.conf import settings
from ZhiHu.settings import Tool
import requests
import json

class Myspider(scrapy.Spider):
    '''初始化各种参数'''
    name='ZhiHu'
    allowed_domains=['zhihu.com']
    L = ''
    K = ''

    All_Num=546049 # 目标抓取量,手动填入
    Save_Num=NumberCheck.find_save() # 已经抓取量
    DB_Num=NumberCheck.find_db_real()  # 上次爬虫，数据库的最后一条数据DB_Num
    Last_Num=NumberCheck.find_last()  # 获得上一次爬虫，轮子哥关注量

    url='https://www.zhihu.com/api/v4/members/excited-vczh/followers?include=data%5B*%5D.locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&limit=20&offset=0'
    response=requests.get(url, headers=settings['DEFAULT_REQUEST_HEADERS'])
    parse=json.loads(response.text)
    try:
        # 获得最新关注者数目Now_Num,注意检验token是否过期
        Now_Num=parse['paging']['totals']
        # 因为关注者不时更新，需计算出真实Real_Num,分两种情况讨论
        # 第一次DB_Num和Last_Num为None,第二次之后不为None
        if DB_Num is not None:
            if Last_Num is not None:
                Real_Num = DB_Num+(Now_Num-Last_Num)-1
                Save_Num = Save_Num
        else:
            Real_Num=All_Num
            Save_Num=0
        print u'目标爬取：', All_Num
        print u'已经抓取：', Save_Num
        print u''
        print u'目前关注：',Now_Num
        print u'上次关注：',Last_Num
    except KeyError:
        print u'\n'
        print u'Authorization过期，请停止程序，重新抓取并在settings中更新'


    def start_requests(self):
        #每隔20页抓一次
        urls=['https://www.zhihu.com/api/v4/members/excited-vczh/followers?include=data%5B*%5D.locations%2Cemployments%2Cgender%2Ceducations%2Cbusiness%2Cvoteup_count%2Cthanked_Count%2Cfollower_count%2Cfollowing_count%2Ccover_url%2Cfollowing_topic_count%2Cfollowing_question_count%2Cfollowing_favlists_count%2Cfollowing_columns_count%2Cavatar_hue%2Canswer_count%2Carticles_count%2Cpins_count%2Cquestion_count%2Ccommercial_question_count%2Cfavorite_count%2Cfavorited_count%2Clogs_count%2Cmarked_answers_count%2Cmarked_answers_text%2Cmessage_thread_token%2Caccount_status%2Cis_active%2Cis_force_renamed%2Cis_bind_sina%2Csina_weibo_url%2Csina_weibo_name%2Cshow_sina_weibo%2Cis_blocking%2Cis_blocked%2Cis_following%2Cis_followed%2Cmutual_followees_count%2Cvote_to_count%2Cvote_from_count%2Cthank_to_count%2Cthank_from_count%2Cthanked_count%2Cdescription%2Chosted_live_count%2Cparticipated_live_count%2Callow_message%2Cindustry_category%2Corg_name%2Corg_homepage%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&limit=20&offset='+str(i)for i in range(0,self.Real_Num)[::-1]]
        for url in urls:
            yield Request(url,callback=self.parse)

    def parse(self,response):
        '''解析json格式数据，获得各类数据'''
        data=json.loads(response.text)['data']
        i=data[0]

        item=ZhihuItem()

        item['Save_Num']=self.Save_Num + 1
        item['Last_Num']=self.Now_Num
        item['Real_Num']=self.Real_Num
        item['name']=i['name']

        #提取标签、个人简介中的文本,用到自定义的Tool类
        tool=Tool()
        item['headline']=tool.replace(i['headline'])
        item['description']=tool.replace(i['description'])

        item['detailURL']='https://www.zhihu.com/people/'+str(i['url_token'])
        item['gender']=i['gender']
        item['user_type']=i['user_type']
        item['is_active']=i['is_active']

        if len(i['locations'])== 0:
            item['locations']=''
        else:
            for n in i['locations']:
                item['locations']=n['name']

        try:
            item['business']=i['business']['name']
        except KeyError:
            item['business']=''

        #教育经历，分多种情况讨论
        if len(i['educations'])== 0:
            item['educations']=''
        else:
            content=[]
            for n in i['educations']:
                S='school' in n.keys()
                M='major' in n.keys()
                if S:
                    if M:
                        self.L=n['school']['name']+'/'+n['major']['name']
                    else:
                        self.L=n['school']['name']
                else:
                    self.L=n['major']['name']
                content.append(self.L)
            item['educations']=''
            for l in content:
                item['educations']+=l+'  '

        #职业经历，分多种情况讨论
        if len(i['employments'])== 0:
            item['employments']=''
        else:
            content=[]
            for n in i['employments']:
                C='company' in n.keys()
                J='job' in n.keys()

                if C:
                    if J:
                        self.K=n['company']['name']+'/'+n['job']['name']
                    else:
                        self.K=n['company']['name']
                else:
                    if J:
                        self.K=n['job']['name']
                content.append(self.K)
                item['employments']=''
                for k in content:
                    item['employments']+=k+'  '

        item['following_count']=i['following_count']
        item['follower_count']=i['follower_count']
        item['mutual_followees_count']=i['mutual_followees_count']

        item['voteup_count']=i['voteup_count']
        item['thanked_count']=i['thanked_count']
        item['favorited_count']=i['favorited_count']
        item['logs_count']=i['logs_count']

        item['following_question_count']=i['following_question_count']
        item['following_topic_count']=i['following_topic_count']
        item['following_favlists_count']=i['following_favlists_count']
        item['following_columns_count']=i['following_columns_count']

        item['articles_count']=i['articles_count']
        item['question_count']=i['question_count']
        item['answer_count']=i['answer_count']
        item['pins_count']=i['pins_count']

        item['participated_live_count']=i['participated_live_count']
        item['hosted_live_count']=i['hosted_live_count']

        print u'序号：', self.Real_Num
        self.Real_Num-= 1
        return item
