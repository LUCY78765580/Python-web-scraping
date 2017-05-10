# -*-coding:utf-8 -*-
#导入settings中各种参数
from ZhiHu import settings
import mysql.connector

# 使用connector连接到数据库
db=mysql.connector.Connect(user=settings.MYSQL_USER, host=settings.MYSQL_HOST, port=settings.MYSQL_PORT,password=settings.MYSQL_PASSWORD, database=settings.MYSQL_DB_NAME)
# 初始化操作游标，buffer指的是使用客户端的缓冲区，减少本机服务器的压力
cursor=db.cursor(buffered=True)

print u'成功连接数据库！'

class MySql(object):
    @classmethod
    def insert_db(cls,item):
        '''数据插入数据库，用到装饰器'''
        sql="INSERT INTO zhihu(Save_Num,Last_Num,Real_Num,name,headline,description,detailURL,gender,user_type,is_active,locations,business,educations,employments,following_count,follower_count,mutual_followees_count,voteup_count,thanked_count,favorited_count,logs_count,following_question_count,following_topic_count,following_favlists_count,following_columns_count,question_count,answer_count,articles_count,pins_count,participated_live_count,hosted_live_count) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values=(item['Save_Num'],item['Last_Num'],item['Real_Num'],item['name'], item['headline'], item['description'], item['detailURL'], item['gender'],
                item['user_type'], item['is_active'], item['locations'], item['business'],
                item['educations'], item['employments'], item['following_count'], item['follower_count'],
                item['mutual_followees_count'], item['voteup_count'], item['thanked_count'], item['favorited_count'],
                item['logs_count'], item['following_question_count'], item['following_topic_count'],
                item['following_favlists_count'], item['following_columns_count'], item['articles_count'],
                item['question_count'], item['answer_count'], item['pins_count'], item['participated_live_count'],
                item['hosted_live_count'])
        cursor.execute(sql,values)
        db.commit()

class NumberCheck(object):
    @classmethod
    def find_db_real(cls):
        '''用于每次断点爬虫前，检查数据库中最新插入的一条数据，
        返回最后一条数据的序号'''
        sql="SELECT Real_Num FROM zhihu ORDER BY Save_Num DESC LIMIT 1;"
        cursor.execute(sql)
        result=cursor.fetchall()  #fetchall返回所有数据列表
        for row in result:
            db_num=row[0]
            return db_num

    @classmethod
    def find_last(cls):
        '''用于每次断点爬虫前，检查数据库中最新插入的一条数据，
        返回上次关注量'''
        sql = "SELECT Last_Num FROM zhihu ORDER BY Save_Num DESC LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            last_num = row[0]
            return last_num

    @classmethod
    def find_save(cls):
        '''用于每次断点爬虫前，检查数据库中最新插入的一条数据，
        返回总共抓取量'''
        sql = "SELECT Save_Num FROM zhihu ORDER BY Save_Num  DESC LIMIT 1;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            save_num = row[0]
            return save_num
