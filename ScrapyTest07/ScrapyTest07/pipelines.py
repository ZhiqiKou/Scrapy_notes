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
            self.cursor.execute("INSERT INTO my_qzone (content,created_time,location_name,location_pos_x,location_pos_y,source_name) VALUES (%s,%s,%s,%s,%s,%s)",(item['content'],item['created_time'],item['location_name'],item['location_pos_x'],item['location_pos_y'],item['source_name']))     # 提交信息
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
