# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
import base64

from ScrapyTest02.settings import USER_AGENTS
from ScrapyTest02.settings import PROXIES

# 随机的User-Agent
class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        #print useragent
        request.headers.setdefault("User-Agent", useragent)

# class RandomProxy(object):
#     def process_request(self, request, spider):
#         proxy = random.choice(PROXIES)
#
#         if proxy['user_passwd'] is None:
#             # 没有代理账户验证的代理使用方式
#             request.meta['proxy'] = "http://" + proxy['ip_port']
#
#         else:
#             # 对账户密码进行base64编码转换
#             base64_userpasswd = base64.b64encode(proxy['user_passwd'])
#             # 对应到代理服务器的信令格式里
#             request.headers['Proxy-Authorization'] = 'Basic ' + base64_userpasswd
#
#             request.meta['proxy'] = "http://" + proxy['ip_port']