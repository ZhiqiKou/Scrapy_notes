# -*- coding: utf-8 -*-
import scrapy


class ZhihuloginSpider(scrapy.Spider):
    name = 'zhihuLogin'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/inbox']

    cookies = {
        'UM_distinctid': '162xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        '__DAYU_PP': 'yxxxxxxxxxxxxxxxxxxxxxd',
        '_zap': 'f50cxxxxxxxxxxxxxxxxxxxxxx048',
        'z_c0': '"2|xxxxxxxxxxxxxxxxxxxxx|92:MixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxX01ORzZnWVFTMGxOdF9B|5f5bxxxxxxxxxxxxxxxxxxxxxxxxx417"',
        'CNZZDATA1256793290': '59643xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx524016409',
        'd_c0': '"AOxxxxxxxxxxxxxxxxxxxxxxxxxxxxx728"',
        'Hm_lvt_0bd5xxxxxxxxxxxxxxxxxxxxxxxxxxxxx14379',
        'q_c1': '00cxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx9756000',
        '_xsrf': 'd4xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxbjP',
        '__utma': '518xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx89.2',
        '__utmz': '51854390.1533xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx|utmcct=/',
        '__utmv': '5185xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx160510=1',
        'tgw_l7_route': '156dxxxxxxxxxxxxxxxxxxxxxxxxf36',
    }

    # 重写Spider类的start_requests方法，附带Cookie值，发送POST请求
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.FormRequest(url, cookies=self.cookies, callback=self.parse_page)

    # 处理响应内容
    def parse_page(self, response):
        with open("zhihu.html", "wb") as filename:
            filename.write(response.body)
