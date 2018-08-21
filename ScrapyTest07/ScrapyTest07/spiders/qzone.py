# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
import time
import json
from ScrapyTest07.items import Scrapytest07Item

class QzoneSpider(scrapy.Spider):
    name = 'qzone'
    allowed_domains = ['qq.com']

    def __init__(self):
        self.cookies = ''
        self.page_num = 0
        self.g_tk = ''

    def start_requests(self):
        browser = webdriver.Chrome()
        browser.get('https://user.qzone.qq.com')
        # 登录表单在页面的框架中，所以要切换到该框架
        browser.switch_to.frame('login_frame')
        browser.find_element_by_id('switcher_plogin').click()
        browser.find_element_by_id('u').send_keys('QQ')
        browser.find_element_by_id('p').send_keys('密码')
        browser.find_element_by_id('login_button').click()
        time.sleep(2)
        try:
            # 得到验证码图片
            bg_link = browser.find_element_by_id('slideBkg').get_attribute('src')
            block_link = browser.find_element_by_id('slideBlock').get_attribute('src')
            time.sleep(10)
            print(bg_link, block_link)
        except:
            pass
        # 获得 gtk
        cookie = {}  # 初始化cookie字典
        self.cookies = browser.get_cookies()
        for elem in self.cookies:  # 取cookies
            cookie[elem['name']] = elem['value']

        self.g_tk = self.getGTK(cookie)  # 通过getGTK函数计算gtk
        browser.close()
        # https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=QQ号&pos=0&num=20&g_tk=438032980
        start_url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=QQ号&pos=0&num=20&g_tk=' + str(self.g_tk)
        yield scrapy.Request(start_url, cookies=self.cookies, callback=self.get_msg)

    def getGTK(self, cookie):
        hashes = 5381
        for letter in cookie['p_skey']:
            hashes += (hashes << 5) + ord(letter)
        return hashes & 0x7fffffff

    def get_msg(self, response):
        response_fix = response.body.decode('utf-8')[10:-2]
        # print(response_fix)
        jsonBody = json.loads(response_fix)
        msglist = jsonBody['msglist']
        if msglist != None:
            for msg in msglist:
                item = Scrapytest07Item()
                item['content'] = msg['content']
                # 转换成localtime
                time_local = time.localtime(int(msg['created_time']))
                # 转换成新的时间格式(XXXX-XX-XX XX:XX:XX)
                dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
                item['created_time'] = dt
                item['location_name'] = msg['lbs']['name']
                item['location_pos_x'] = msg['lbs']['pos_x']
                item['location_pos_y'] = msg['lbs']['pos_y']
                item['source_name'] = msg['source_name']
                print(item)
                yield item
            self.page_num += 1
            url = 'https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=QQ号&pos=' + str(self.page_num * 20) + '&num=20&g_tk=' + str(self.g_tk)
            yield scrapy.Request(url, cookies=self.cookies, callback=self.get_msg)
        else:
            print('全部数据获取完毕！')

