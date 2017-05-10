# -*- coding: utf-8 -*-
import scrapy
class ZhihuItem(scrapy.Item):
    Save_Num=scrapy.Field()  #总共抓取数据
    Last_Num=scrapy.Field()  #记录本次关注者
    Real_Num=scrapy.Field()  #真实的序号
    name=scrapy.Field()  #名字
    headline=scrapy.Field()  #个性签名
    description=scrapy.Field()  #个人简介
    detailURL=scrapy.Field()  #主页地址
    gender=scrapy.Field()  #等级
    user_type=scrapy.Field()  #用户类型
    is_active=scrapy.Field()  #是否活跃用户
    locations=scrapy.Field()  #居住地
    business=scrapy.Field()  #行业
    educations=scrapy.Field()  #教育经历
    employments=scrapy.Field()  #职业经历
    following_count=scrapy.Field()  #他关注的人
    follower_count=scrapy.Field()  #关注他的人
    mutual_followees_count=scrapy.Field()  #我和他共同关注的人
    voteup_count=scrapy.Field()  #赞同
    thanked_count=scrapy.Field()  #感谢
    favorited_count=scrapy.Field() #收藏
    logs_count=scrapy.Field()  #公共编辑
    following_question_count=scrapy.Field()  #关注的问题
    following_topic_count=scrapy.Field()  #关注的话题
    following_favlists_count=scrapy.Field()  #关注的收藏夹
    following_columns_count=scrapy.Field()  #关注的专栏
    question_count=scrapy.Field()  #提问
    answer_count=scrapy.Field()  #回答
    articles_count=scrapy.Field()  #文章
    pins_count=scrapy.Field()  #分享
    participated_live_count=scrapy.Field()  #参加的live
    hosted_live_count=scrapy.Field()  #举办的live







