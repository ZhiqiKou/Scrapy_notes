# -*- coding: utf-8 -*-
import scrapy
from DaiLi.items import DailiItem
import requests


class XiciSpider(scrapy.Spider):
    name = 'xici'
    allowed_domains = ['xicidaili.com']
    start_urls = []
    for i in range(1, 6):
        start_urls.append('http://www.xicidaili.com/nn/' + str(i))

    def parse(self, response):
        ip = response.xpath('//tr[@class]/td[2]/text()').extract()
        port = response.xpath('//tr[@class]/td[3]/text()').extract()
        agreement_type = response.xpath('//tr[@class]/td[6]/text()').extract()
        proxies = zip(ip, port, agreement_type)
        # print(proxies)

        # 验证代理是否可用
        for ip, port, agreement_type in proxies:
            proxy = {'http': agreement_type.lower() + '://' + ip + ':' + port,
                     'https': agreement_type.lower() + '://' + ip + ':' + port}
            try:
                # 设置代理链接  如果状态码为200 则表示该代理可以使用
                print(proxy)
                resp = requests.get('http://icanhazip.com', proxies=proxy, timeout=2)
                print(resp.status_code)
                if resp.status_code == 200:
                    print(resp.text)
                    # print('success %s' % ip)
                    item = DailiItem()
                    item['proxy'] = proxy #agreement_type + '://' + ip + ':' + port
                    #print(item['proxy'])
                    yield item
            except:
                print('fail %s' % ip)

