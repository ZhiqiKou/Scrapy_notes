# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import redis

class DyttRedisMasterPipeline(object):
    def __init__(self):
        # 初始化连接数据的变量
        self.REDIS_HOST = '127.0.0.1'
        self.REDIS_PORT = 6379
        # 链接redis
        self.r = redis.Redis(host=self.REDIS_HOST, port=self.REDIS_PORT)

    def process_item(self, item, spider):
        # 向redis中插入需要爬取的链接地址
        self.r.lpush('dytt:start_urls', item['url'])
        return item
