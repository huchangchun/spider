# -*- coding:utf-8 -*-
import requests
#get请求添加头文件伪装浏览器
payload = {'key1':'values1','key2':'values2'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
re = requests.get('http://httpbin.org/get',params=payload,headers=headers)
print(re.text)
print(re.url)

#伪装浏览器访问知乎网站
re = requests.get("https://www.zhihu.com",headers=headers)
# print(re.text)