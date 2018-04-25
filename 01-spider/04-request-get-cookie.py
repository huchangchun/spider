# -*- coding:utf-8 -*-
"""
GET 请求，获取网页cookie
"""
import requests
url = 'http://httpbin.org/cookies'
re = requests.get(url,cookies={'name':'joe'})
print(re.text)


