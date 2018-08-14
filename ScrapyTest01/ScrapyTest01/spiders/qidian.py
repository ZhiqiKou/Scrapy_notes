# -*- coding: utf-8 -*-
import scrapy
from ScrapyTest01.items import Scrapytest01Item


class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['qidian.com/']
    start_urls = ['https://www.qidian.com/rank/hotsales']

    def parse(self, response):
        # with open('book.html', 'w') as f:
        #      f.write(response.body.decode('utf-8'))


        # 存放书籍的集合
        book_items = []

        # item = Scrapytest01Item()
        # title = response.xpath("//div[@class='book-mid-info']/h4/a/text()").extract()
        # author = response.xpath("//div[@class='book-mid-info']/p/a[@class='name']/text()").extract()
        # abstract = response.xpath("//div[@class='book-mid-info']/p[@class='intro']/text()").extract()
        #
        # item['title'] = title
        # item['author'] = author
        # item['abstract'] = abstract
        #
        # book_items.append(item)

        for each in response.xpath("//div[@class='book-mid-info']"):
            item = Scrapytest01Item()
            title = each.xpath("h4/a/text()").extract()[0]
            author = each.xpath("p/a[@class='name']/text()").extract()[0]
            abstract = each.xpath("p[@class='intro']/text()").extract()[0].strip()
            item['title'] = title
            item['author'] = author
            item['abstract'] = abstract

            book_items.append(item)

        return book_items