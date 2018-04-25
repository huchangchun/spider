# -*- coding:utf-8 -*-
"""
compile() 返回一个对象的模式
match()
从字符串的开头进行匹配，匹配成功就返回一个匹配对象，失败返回None
"""
import re
# pattern = re.compile('\w\w')
# print(type(pattern))

#match匹配开头
# print(re.match('hello','hello joe').group())

pattern = re.compile('hello')
# str = 'hello world'
# print(pattern.match(str).group())

# strs='hello world hello'
# print(pattern.match(strs).group())  #只匹配开头

#search　只匹配一次，成功后不继续匹配
# pattern = re.compile('[a-z]{3}')
# strs = '123666'
# print(pattern.search(strs)) #匹配不成功返回None
# strs ='123abc343'
# print(pattern.search(strs).group())

#findall()遍历匹配
# pattern = re.compile('[a-z]{3}')
# strs = '123abc666def12cde32'
# print(pattern.findall(strs))
# # ['abc', 'def', 'cde']

#遇上分组时返回分组结果
# pattern = re.compile('(\d+)[a-z]{3}')
# strs = '123abc666def12cde32'
# print(pattern.findall(strs))
# ['123', '666', '12']

#finditer()返回一个顺序访问每一个匹配结果（match)对象的迭代器
#找到re匹配的所有子串，并把他们作为一个迭代器返回
pattern= re.compile('([a-z])[a-z]([a-z])') #匹配任意长度英文字母
str1='123abc456def789'
result = pattern.finditer(str1)
print(result)
for i in result:
    print(i.group(0))
    print(i.group(1))
    print(i.group(2))
#split()按照能够匹配的子串将string分割后返回列表
print(re.split('\d+','one11two2three3'))
print(re.split('\W+','one,2two,three,four'))

#sub()使用re替换string中的每一个匹配的子串后返回替换的字符串
print(re.sub('\d+','-','one11two2three3'))
#subn()返回替换的结果和替换次数
print(re.subn('\d+','-','one11two2three3'))

#引用分组 \1表示第一个分组，\2表示第二个分组
strs = 'hello 123,world 321'
pattern = re.compile('(\w+)(\d+)')
for i in pattern.finditer(strs):
    print(i.group(0))
    print(i.group(1))
    print(i.group(2))
print(pattern.sub(r'\2 \1',strs)) #取得分组\1 \2


#贪婪与非贪婪
str1 = 'aaa<p>hello</p>bbb<p>world</p>ccc'
pattern = re.compile('<p>.*</p>')  #.匹配任意字符*0-无限次
print(pattern.findall(str1))  #贪婪模式
# ['<p>hello</p>bbb<p>world</p>']
pattern=re.compile('<p>.*?</p>')
print(pattern.findall(str1))  #非贪婪模式，尽可能少的匹配，遇到结束的标签则结束
# ['<p>hello</p>', '<p>world</p>']

##匹配中文字符
str1 = '你好，hello,哥哥'
pattern = re.compile('\w+')
print(pattern.findall(str1))
# ['你好', 'hello', '哥哥']
pattern = re.compile('[\u4e00-\u9fa5]+')#匹配中文字符
print(pattern.findall(str1))
# ['你好', '哥哥']