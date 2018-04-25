# -*- coding:utf-8 -*-
import requests
'''
HTTP协议是一中无状态的协议，为了维持客户端与服务器之间的通信状态，
使用 Cookie 技术使之保持双方的通信状态。
有些网页是需要登录才能进行爬虫操作的，
而登录的原理就是浏览器首次通过用户名密码登录之后，
服务器给客户端发送一个随机的Cookie，下次浏览器请求其它页面时，
就把刚才的 cookie 随着请求一起发送给服务器，这样服务器就知道该用户已经是登录用户。
'''
#构建会话

session=requests.Session()
url = 'http://httpbin.org/get'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
re = session.get(url,headers=headers)
# print(re.text)
session.headers.update(headers)
re = session.get(url,headers={'cookes':'two'})
# print(re.text)


"""
timeout
"""
from requests.exceptions import  ConnectTimeout,ConnectionError,RequestException
try:
    re = requests.get('http://github.com',timeout=0.5)
    # print(re.status_code)
except ConnectTimeout:
    print('Time out')
except ConnectionError:
    print('connect error')
except RequestException as e:
    print(e)

"""
代理
"""
proxies = {"http":"http://182.110.154.75:61202",
           "https":"http://119.28.138.104:3128"}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
# re = requests.get('http://httpbin.org/get',proxies=proxies,headers=headers)
# print(re.text)

try:
    re = requests.get('https://www.taobao.com/get', proxies=proxies, headers=headers,timeout=0.1)
    print(re.text)
except ConnectTimeout:
    print('Time out')
except ConnectionError:
    print('connect error')
except RequestException as e:
    print(e)


"""
ssl验证
"""
re = requests.get('https://www.12306.cn', verify=False)
print(re.status_code)
print(re.content.decode('UTF-8'))
