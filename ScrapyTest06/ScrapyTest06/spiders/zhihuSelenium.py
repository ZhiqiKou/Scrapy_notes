# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time

class ZhihuseleniumSpider(scrapy.Spider):
    name = 'zhihuSelenium'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/inbox']

    def start_requests(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(chrome_options=chrome_options)
        browser.get('https://www.zhihu.com/signup')
        # 切换到登陆
        browser.find_element_by_xpath("//div[@class ='SignContainer-switch']/span").click()
        # 输入账号
        browser.find_element_by_name("username").send_keys("1XXXXXXXXXX")
        # 输入密码
        browser.find_element_by_name("password").send_keys("XXXXXXXXXXXXXXX")
        # 点击登陆按钮
        browser.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)  # 等待登陆跳转
        cookies = browser.get_cookies()
        browser.close()
        for url in self.start_urls:
            yield scrapy.FormRequest(url, cookies=cookies, callback=self.parse_page)

    # 处理响应内容
    def parse_page(self, response):
        with open("zhihu.html", "wb") as filename:
            filename.write(response.body)