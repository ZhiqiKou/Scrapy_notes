# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Scrapytest02Item(scrapy.Item):
    # 书名
    title = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 作品信息
    information = scrapy.Field()
    # 作品简介
    Introduction = scrapy.Field()
    # 字数
    word_num = scrapy.Field()
    # 点击量
    clicks_num = scrapy.Field()
    # 推荐数
    recommended_num = scrapy.Field()


