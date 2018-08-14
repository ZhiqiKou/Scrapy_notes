# -*- coding: utf-8 -*-
import scrapy
import re
from io import BytesIO
from PIL import Image

class DoubanloginSpider(scrapy.Spider):
    name = 'doubanLogin'
    allowed_domains = ['douban.com']
    start_urls = ['https://accounts.douban.com/login']

    def parse(self, response):
        temp = {}
        captcha = response.xpath('//img[@id = "captcha_image"]/@src').extract()
        if captcha:
            # 有验证码
            temp['captcha'] = captcha[0]
            temp['response'] = response
            print(captcha)
            yield scrapy.Request(captcha, callback=self.get_captcha, meta=temp)
        else:
            # 没有验证码
            yield scrapy.FormRequest.from_response(
                response,
                formdata={
                    "source": "index_nav",
                    # "redir": "https://www.douban.com/people/182875833/",
                    "form_email": "1XXXXXXXXXXX",
                    "form_password": "zXXXXXXXXXX!",
                    "user_login": "登录"
                },
                callback=self.parse_page
            )


    def get_captcha(self, response):
        captcha_img = Image.open(BytesIO(response.body))
        captcha_img.show()

        captcha_id = re.search(r'id=\w+:en', response.meta['captcha']).group(0).split('=')[1]
        captcha_solution = input("请输入验证码：")
        # 发送请求参数，并调用指定回调函数处理
        yield scrapy.FormRequest.from_response(
            response.meta['response'],
            formdata={
                "source": "index_nav",
                # "redir": "https://www.douban.com/people/182875833/",
                "form_email": "1XXXXXXXXXX",
                "form_password": "zxXXXXXXXX!",
                "captcha-solution": captcha_solution,
                "captcha-id": captcha_id,
                "user_login": "登录"
            },
            callback=self.parse_page
        )

    def parse_page(self, response):
        url = "https://www.douban.com/people/182875833/"
        yield scrapy.Request(url, callback=self.parse_newpage)

    def parse_newpage(self, response):
        with open("people.html", 'wb') as f:
            f.write(response.body)
