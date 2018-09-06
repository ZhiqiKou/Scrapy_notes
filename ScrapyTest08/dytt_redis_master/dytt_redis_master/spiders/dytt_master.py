# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from dytt_redis_master.items import DyttRedisMasterItem

class DyttMasterSpider(CrawlSpider):
    name = 'dytt_master'
    allowed_domains = ['dy2018.com']
    start_urls = ['https://www.dy2018.com/0/']

    rules = (
        Rule(LinkExtractor(allow=r'/\d{1,2}/$'), callback='parse_item'),
    )

    def parse_item(self, response):
        # print(response.url)
        items = DyttRedisMasterItem()
        items['url'] = response.url
        yield items
