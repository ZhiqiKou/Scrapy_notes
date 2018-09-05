# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DyttRedisSlaverItem(scrapy.Item):
    # 译名
    name = scrapy.Field()
    # 年代
    year = scrapy.Field()
    # 语言
    language = scrapy.Field()
    # 上映日期
    release_date = scrapy.Field()
    # 评分
    score = scrapy.Field()
    # 文件大小
    file_size = scrapy.Field()
    # 片长
    film_time = scrapy.Field()
    # 简介
    introduction = scrapy.Field()
    # 海报
    posters = scrapy.Field()
    # 下载链接
    download_link = scrapy.Field()
    # utc时间
    crawled = scrapy.Field()
    # 爬虫名
    spider = scrapy.Field()


