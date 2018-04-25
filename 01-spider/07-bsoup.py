# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import re
rep = requests.get('http://www.baidu.com').content.decode('UTF-8')
# print(re)
soup = BeautifulSoup(rep,'html.parser')  #默认解析器

html = soup.prettify()  #美化格式
print(html)


#四大对象
#1.Tag 标签
# print(soup.div.a)  #获取第一个标签
# print(soup.div.a.name)
# print(soup.div.a.attrs)
# print(soup.div.a.attrs['href'])

"""
遍历文档树
"""
#直接子节点
# print(soup.div.div.div.div.div.div.contents)
# print(soup.div.children)
# for i in soup.div.children:
#     print(i)
# #所有的子孙节点
# print(soup.div.descendants)
# for  i in  soup.div.descendants:
#     print(i)
#获取文本
"""
通过string获取文本是只有在子节点的时候
"""
# print(soup.div.span.string)  #返回None,因为还有子节点

# print(soup.div.div.div.div.div.div)

#find_all
# print(soup.find_all(href=re.compile('www.*')))
# print(soup.find_all(id='u1'))  #id 唯一性
# print(soup.find_all(id='cp'))
# print(soup.find(id='cp'))
# print(soup.find(id='cp').find_all('a'))
# print(soup.find(id='cp').find_all('a')[0]['href'])
# print(soup.find(id='cp').find_all('a')[0].text)


'''
css选择器
'''
soup = BeautifulSoup(open('baidu.html',encoding='utf8') ,'html.parser')
#通过标签
print(soup.select('a'))
#通过类名
print(soup.select('.mnav'))
#通过ID
print(soup.select('#ftCon'))
#属性

#组合查找
