# -*- coding: utf-8 -*-
# Author:cs.liuxiaoqing@gmail.com

import pymysql
import yaml,os

class MySQLCommand(object):
    # 类的初始化
    def __init__(self):
        with open('MySQLSetting.yml','r',encoding='UTF-8') as fp:
            Mysql = yaml.load(fp)
        MySQLInfo = Mysql['MySQL']

        self.host = MySQLInfo['Host']
        self.port = MySQLInfo['Port']               # 端口号
        self.user = MySQLInfo['User']               # 用户名
        self.password = MySQLInfo['Password']       # 密码
        self.db = MySQLInfo['Database']             # 库
        self.Photo_table = MySQLInfo['Tablename']   # 表
        self.use_unicode = MySQLInfo['UseUnicode']
        self.charset = MySQLInfo['Charset']         # 编码使用utf8mb4可以存储emoji表情符号

        # 链接数据库
    def connectMysql(self):
        try:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                        passwd=self.password, db=self.db, charset=self.charset)
            self.cursor = self.conn.cursor()
            print('连接MySQL成功')
        except:
            print('connect mysql error.')

    def creatTable(self):
        #数据表如果之前存在则删除，重新创建数据
        creat_sql = "create table "+self.Photo_table+\
                    " ( Id int auto_increment primary key," \
                    "Photourl VARCHAR(100) NOT NULL," \
                    "Photoid VARCHAR(100) NOT NULL," \
                    "OwnerNickname VARCHAR(255)," \
                    "OwnerRealname VARCHAR(255)," \
                    "OwnerLocation VARCHAR(255)," \
                    "OwnerTimezone VARCHAR(255)," \
                    "Postdate VARCHAR(255)," \
                    "Geolatitude VARCHAR(255)," \
                    "Geolongitude VARCHAR(255)," \
                    "Tags TEXT," \
                    "Comments TEXT)AUTO_INCREMENT=1"


        delete_sql = "drop table if exists "+ self.Photo_table
        self.cursor.execute(delete_sql)
        self.cursor.execute(creat_sql)
        print('创建MySQL成功')


    def insertData(self,PhotoUrl,PhotoId,
                   OwnerNickname,OwnerRealname,Postdate,
                   OwnerTimezone,OwnerLocation,Geolatitude,
                   Geolongitude,Tags,Comments):
        try:

            table = self.Photo_table
            photo_property = "Photourl,Photoid," \
                             "OwnerNickname,OwnerRealname," \
                             "Postdate,OwnerLocation,OwnerTimezone,Geolatitude," \
                             "Geolongitude,Tags,Comments"

            OwnerNickname = self.conn.escape(OwnerNickname)
            OwnerRealname = self.conn.escape(OwnerRealname)
            Tags = self.conn.escape(Tags)
            Comments = self.conn.escape(Comments)

            photo_data = '"'+PhotoUrl+'"'+','\
                         +'"'+PhotoId+'"'+','\
                         +'"'+OwnerNickname+'"'+','\
                         +'"'+OwnerRealname+'"'+','\
                         +'"'+Postdate+'"'+',' \
                         +'"'+OwnerLocation+'"'+',' \
                         +'"'+OwnerTimezone+'"'+',' \
                         +'"'+Geolatitude+'"'+','\
                         +'"'+Geolongitude+'"'+','\
                         +'"'+Tags+'"'+','\
                         +'"'+Comments+'"'

            sql = "INSERT INTO "+ table + "(%s) VALUES (%s)" %(photo_property,photo_data)
            result = self.cursor.execute(sql)
            id = str(self.conn.insert_id())
            self.conn.commit()
            if result==1:

                return id
            else:
                return '0'
        except:
            return '0'


    def deleteInfo(self,ID):

        result = dict()

        sql = "DELETE FROM " + self.Photo_table + " WHERE Id = '%d'" %(ID)
        backInfo = self.cursor.execute(sql)
        self.conn.commit()
        result['stat'] = backInfo
        if backInfo==1:
            result['msg'] = '已将'+str(ID)+'从数据库中删除！'
        else:
            result['msg'] = '删除'+str(ID)+'失败！'
        return result