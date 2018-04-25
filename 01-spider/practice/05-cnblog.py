# -*- coding:utf-8 -*-
from lxml import etree
import requests
from bs4 import BeautifulSoup
"""
获取博客园 每一帖子的标题和内容
分析：
    1、入口：https://www.cnblogs.com/
    2、获取每一个帖子的url
    3、通过url访问每一篇帖子，获取标题和内容
    //a[@id="cb_post_title_url"]/text()
     //string(//a[@id="cnblogs_post_body"])
"""
base = 'https://www.cnblogs.com'
url = 'https://www.cnblogs.com/sitehome/p/1'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

num = 1
page =1
while True:
    rep = requests.get(url,headers=headers).content.decode('UTF-8')
    html = etree.HTML(rep)
    urllist = html.xpath("//a[@class='titlelnk']/@href")

    for suburl in urllist:
        num += 1
        print('第{0}页第{1}篇帖子'.format(page, num))
        subr = requests.get(suburl, headers=headers).text

        htmls = etree.HTML(subr)

        # 获取标题
        title = htmls.xpath("string(//a[@id='cb_post_title_url'])")
        # print(title)
        # 获取内容
        content = htmls.xpath("string(//div[@id='cnblogs_post_body'])")
        # print(content)

        with open('cn-blogs.txt','+a',encoding='UTF-8') as outputfile:
            outputfile.write('\n' + '='*200 + '\n')
            outputfile.write('第{0}页第{1}篇帖子\n'.format(page, num))
            outputfile.write(title + '\n')
            outputfile.write(content + '\n')
            outputfile.write('\n' +'-'*200 + '\n')
        num +=1
        # 获取下一页
    next_page = html.xpath("//div[@class='pager']/a[last()]")
    next = next_page[0].xpath('text()')
    if next[0] == 'Next >':
        page += 1
        num = 1
        url = base + next_page[0].xpath('@href')[0]
        print(url)
    else:
        break
