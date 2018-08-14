# -*- coding: utf-8 -*-
import scrapy
from ScrapyTest02.items import Scrapytest02Item
from lxml import etree
import re
from fontTools.ttLib import TTFont
from io import BytesIO

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# class QidianFontSpider(scrapy.Spider):
class QidianFontSpider(CrawlSpider):
    name = 'qidian_font'
    allowed_domains = ['qidian.com', 'qidian.gtimg.com']
    # start_urls = ['https://book.qidian.com/info/1010191960']

    start_urls = []
    for i in range(1, 26):
        start_urls.append('https://www.qidian.com/rank/hotsales?page=' + str(i))

    rules = (
        Rule(LinkExtractor(allow=r'info/\d+'), callback='parse_item'),
    )

    def __init__(self,*args, **kwargs):
        self.WORD_TO_NUM = {"zero": "0","one": "1","two": "2","three":"3","four":"4","five":"5","six":"6","seven":"7","eight":"8","nine":"9","period":"."}

        super(QidianFontSpider, self).__init__(*args, **kwargs)  # crawlSpider一定要加上这句
        self.font_dic = {}

    def parse_item(self, response):

        #item = Scrapytest02Item()
        title = response.xpath('//div[@class="book-info "]/h1/em/text()').extract()[0]
        author = response.xpath('//div[@class="book-info "]//a[@class="writer"]/text()').extract()[0]
        information = response.xpath('//div[@class="book-info "]/p[@class="intro"]/text()').extract()[0]
        Introduction = response.xpath('//div[@class="book-intro"]//p/text()').extract()[0].strip()
        # word_num = response.xpath('//div[@class="book-info "]/p[3]/em[1]/span/text()').extract()[0]
        # clicks_num = response.xpath('//div[@class="book-info "]/p[3]/em[2]/span/text()').extract()[0]
        # recommended_num = response.xpath('//div[@class="book-info "]/p[3]/em[3]/span/text()').extract()[0]
        #
        # item['title'] = title
        # item['author'] = author
        # item['information'] = information
        # item['Introduction'] = Introduction
        # item['word_num'] = word_num
        # item['clicks_num'] = clicks_num
        # item['recommended_num'] = recommended_num
        #
        # yield item

        # 得到字体的名字
        font_style = response.xpath('//div[@class="book-info "]//style/text()').extract()[0]
        font_name = font_style.split(';')[0].split(':')[1].strip()

        html = etree.HTML(response.text)
        # 获取文章字数字体的编码
        word_num_coding = self.get_coding(html, 'p[3]/em[1]/span')
        # 获取文章点击量字体的编码
        clicks_num_coding = self.get_coding(html, 'p[3]/em[2]/span')
        # 获取文章总推荐字体的编码
        recommended_num_coding = self.get_coding(html, 'p[3]/em[3]/span')

        # 临时的字典，用于回调传参
        temp = {}
        temp['word_num_coding'] = word_num_coding
        temp['clicks_num_coding'] = clicks_num_coding
        temp['recommended_num_coding'] = recommended_num_coding
        temp['title'] = title
        temp['author'] = author
        temp['information'] = information
        temp['Introduction'] = Introduction

        font_link = 'https://qidian.gtimg.com/qd_anti_spider/' + font_name + '.woff'
        if font_link not in self.font_dic.keys():
            yield scrapy.Request(font_link, callback=self.parse_detial, meta=temp, dont_filter=True)
        else:
            yield self.processing_data(self.font_dic.get(font_link), temp)

    def get_coding(self,html, word_num_title_xpath):
        # 文章信息的根节点
        root_node = html.xpath('//div[@class="book-info "]')
        # 字数标签
        num_title = root_node[0].find(word_num_title_xpath)
        # 字数标签解码
        num_text = etree.tostring(num_title).decode()
        # 正则匹配
        groups = re.search(r'>(.*?);<', num_text)
        # 取出字数的字码
        num_coding = groups[1]
        # 返回字数的字码
        return num_coding

    def parse_detial(self, response):
        font = TTFont(BytesIO(response.body))
        cmap = font.getBestCmap()
        font.close()
        self.font_dic[response.url] = cmap

        return self.processing_data(cmap, response.meta)

    def processing_data(self, cmap, meta):
        word_num = self.decode_num(cmap, meta, 'word_num_coding')
        clicks_num = self.decode_num(cmap, meta, 'clicks_num_coding')
        recommended_num = self.decode_num(cmap, meta, 'recommended_num_coding')
        item = Scrapytest02Item()
        item['title'] = meta.get('title')
        item['author'] = meta.get('author')
        item['information'] = meta.get('information')
        item['Introduction'] = meta.get('Introduction')
        item['word_num'] = word_num + '万字'
        item['clicks_num'] = clicks_num + '万总会员点击'
        item['recommended_num'] = recommended_num + '万总推荐'
        return item

    def decode_num(self, cmap, meta,code_name):
        word_num = ''
        num_coding_list = meta.get(code_name).replace('&#', '').split(';')
        for num in num_coding_list:
            ch = cmap.get(int(num))
            word_num += self.WORD_TO_NUM[ch]
        return word_num