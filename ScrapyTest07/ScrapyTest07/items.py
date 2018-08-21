# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapytest07Item(scrapy.Item):
    # 说说内容
    content = scrapy.Field()
    # 发表时间
    created_time = scrapy.Field()
    # 发表地点
    location_name = scrapy.Field()
    # 经度
    location_pos_x = scrapy.Field()
    # 纬度
    location_pos_y = scrapy.Field()
    # 设备
    source_name = scrapy.Field()
