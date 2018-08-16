# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import base64
from io import BytesIO
from PIL import Image
import random
import re


class ZhihuseleniumSpider(scrapy.Spider):
    name = 'zhihuSelenium'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/inbox']

    def start_requests(self):
        # chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        # browser = webdriver.Chrome(chrome_options=chrome_options)
        browser = webdriver.Chrome()
        browser.set_window_size(100,100)
        browser.get('https://www.zhihu.com/signup')
        # 切换到登陆
        browser.find_element_by_xpath("//div[@class ='SignContainer-switch']/span").click()
        # 输入账号
        browser.find_element_by_name("username").send_keys("1XXXXXXXXXX")
        # 输入密码
        browser.find_element_by_name("password").send_keys("XXXXXXXXXXXXXXX")
        # 查看是否有验证码
        Captcha_element = browser.find_element_by_xpath("//form[@class='SignFlow']/div[3]//img")
        Captcha_base64 = Captcha_element.get_attribute('src')
        print(Captcha_base64)
        # # 如果有验证码：
        if Captcha_base64 != 'data:image/jpg;base64,null':
            # 得到验证码图片
            img_data1 = Captcha_base64.split(',')[-1]
            data1 = base64.b64decode(img_data1)
            image = Image.open(BytesIO(data1))
            image.show()
            Captcha_type = Captcha_element.get_attribute('class')
            # 如果是英文验证码：
            if Captcha_type == 'Captcha-englishImg':
                # 输入验证码字符并send_keys
                Captcha = input('请输入图片中的验证码：')
                browser.find_element_by_name("captcha").send_keys(Captcha)
            # 否则：
            else:
                # 输入坐标，鼠标模拟点击
                # 每个字宽度约 (160.5-5.5)/7=22
                # 每个字高度范围：13.5———35.5
                handstand = input('请输入倒立文字的序号（以‘,’分割）：')
                handstand_serial_nums = handstand.split(',')
                for handstand_serial_num in handstand_serial_nums:
                    x = 5.5 + (int(handstand_serial_num) - 1) * 22 + random.uniform(10, 20) # 随机一个范围
                    y = random.uniform(15, 30)
                    click_pos = (x, y)
                    print(click_pos)
                    ActionChains(browser).move_to_element_with_offset(Captcha_element, x, y).perform()
                    ActionChains(browser).click().perform()
        # 点击登陆按钮
        browser.find_element_by_xpath("//button[@type='submit']").click()
        time.sleep(2)  # 等待登陆跳转
        print(browser.title)
        # 如果登陆title包含“首页”，登陆成功
        if re.search(r'首页', browser.title):
            print('登陆成功！！')
            cookies = browser.get_cookies()
            browser.close()
            for url in self.start_urls:
                yield scrapy.FormRequest(url, cookies=cookies, callback=self.parse_page)
        else:
            print("登陆失败！")

    # 处理登陆后的响应内容
    def parse_page(self, response):
        with open("zhihu.html", "wb") as filename:
            filename.write(response.body)