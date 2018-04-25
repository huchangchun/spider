# -*- coding:utf-8 -*-
import requests
response = requests.get('http://www.ibeifeng.net')
# print(response.status_code)
# print(response.encoding)
# print(response.cookies)
# print(response.text)
# print(response.content)
# re= requests.post('http://httpbin.org/post')
# print(re.status_code)
# print(re.text)
# re= requests.put('http://httpbin.org/put')
# print(re.status_code)
# print(re.text)

# re= requests.delete('http://httpbin.org/delete')
# print(re.status_code)
# print(re.text)

payload = {'key1':'values1','key2':'values2'}
re= requests.post('http://httpbin.org/post',data=payload)
print(re.text)
