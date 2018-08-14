# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class DBPipeline(object):

    def __init__(self):
        self.connect = pymysql.connect(
            host='localhost',
            db='Scrapy',
            user='root',
            passwd='zhiqi'
        )
        # 数据库游标，用于操作数据库
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        try:
            # 将信息写入数据库
            self.cursor.execute("INSERT INTO ZhPyZnCom(title,author,headline,url) VALUES (%s,%s,%s,%s)",(item['title'],item['name'],item['headline'],item['url']))
            # 提交信息
            self.connect.commit()
        except Exception as e:
            # 输出错误信息
            print(e)

        return item

    def close_spider(self, spider):
        # 关闭游标
        self.cursor.close()
        # 关闭连接
        self.connect.close()
