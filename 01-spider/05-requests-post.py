# -*- coding:utf-8 -*-
import requests
"""
POST请求，传递参数
"""
url = 'http://httpbin.org/post'
datas={'user':'joe','pwd':'123345'}
re = requests.post(url,data=datas)
# print(re.text)

"""
POST请求，发送cookie
"""
url = 'http://httpbin.org/post'
cookies = dict(cookies_are='working')
re = requests.post(url,cookies=cookies)
# print(re.cookies)
# print(re.text)

"""
POST请求，发送文件
"""

url = 'http://httpbin.org/post'
files = {'file':open('a.txt','rb')}
re = requests.post(url,files=files)
# print(re.text)

"""
POST请求，发送json数据
"""
import json
url = 'http://httpbin.org/post'
payload={'some':'data'}
re = requests.post(url,data=json.dumps(payload))
print(re.text)