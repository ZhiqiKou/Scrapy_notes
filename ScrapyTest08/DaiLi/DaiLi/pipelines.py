# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DailiPipeline(object):

    def __init__(self):
        self.file = open('proxy.txt', 'w')

    def process_item(self, item, spider):
        self.file.write(str(item['proxy']) + '\n')
        return item

    def close_spider(self, spider):
        self.file.close()
