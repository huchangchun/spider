# -*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import time
'''
需求：获取runoob python100例当中的所有的例子，标题，题目，分析，源代码

分析：
    1、入口：‘http://www.runoob.com/python/python-100-examples.html’
    2、div ID=content 获取所有的a标签
    3、请求所有的链接
'''
baseurl = 'http://www.runoob.com/python/python-100-examples.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}
rep = requests.get(baseurl,headers=headers).content.decode('UTF-8')

soup = BeautifulSoup(rep,'html.parser')  #默认解析器

# print(soup.find(id="content"))
a = soup.find(id="content").ul.find_all('a')
new_url = []

#通过find_all方式实现
for i in a:
    new_url.append(i.attrs['href'])
# print(new_url)

# for i in new_url:
#     rs = requests.get('http://www.runoob.com' +i,headers=headers).content.decode('utf8')
#     soups = BeautifulSoup(rs,'html.parser')
#     # print(soups)
#     contents ={}
#
#     #找标签
#     contents['title'] = soups.find(id='content').h1.text
#     # print(contents['title'])
#     contents['timu']=soups.find(id='content').find_all('p')[1].text
#     contents['cxfx']=soups.find(id='content').find_all('p')[2].text
#     try:
#         contents['cxym']=soups.find(class_='hl-main').text
#     except:
#         contents['cxym'] = soups.find('pre').text
#     with open('py-practice-100','a+',encoding='utf8') as outputfile:
#         outputfile.write('\n' +'='*50 +'\n')
#         outputfile.write(contents['title'] + '\n')
#         outputfile.write(contents['timu'] + '\n')
#         outputfile.write(contents['cxfx'] + '\n')
#         outputfile.write(contents['cxym'] + '\n')
#         outputfile.write('\n' + '='*50 + '\n')
#     time.sleep(0.2)

#通过select实现
for i in new_url:
    rs = requests.get('http://www.runoob.com' +i,headers=headers).content.decode('utf8')
    soups = BeautifulSoup(rs,'html.parser')
    # print(soups)
    contents ={}

    #找标签
    contents['title'] = soups.select('#content h1')[0].text
    # print(contents['title'])
    contents['timu']=soups.select('#content p')[1].text
    contents['cxfx']=soups.select('#content p')[2].text  #查找id 为content 下的p标签
    try:
        contents['cxym']=soups.select('.hl-main')[0].text  #查找类名 .类名
    except:
        contents['cxym'] = soups.select('pre')[0].text
    with open('runoob-100.txt','a+',encoding='utf8') as outputfile:
        outputfile.write('\n' +'='*50 +'\n')
        outputfile.write(contents['title'] + '\n')
        outputfile.write(contents['timu'] + '\n')
        outputfile.write(contents['cxfx'] + '\n')
        outputfile.write(contents['cxym'] + '\n')
        outputfile.write('\n' + '='*50 + '\n')
    time.sleep(0.2)