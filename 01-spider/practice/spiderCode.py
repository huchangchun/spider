# -*- coding:utf-8 -*-
"""
获取邮编
"""

import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
#获取etree
def get_html_by_etree(url,headers):
    return etree.HTML(requests.get(url,headers=headers).content.decode('utf-8'))
def getCode(content):
    contentCode = int(content[0].strip().split("\n")[0])   
    return contentCode
def start(url,headers):
    selector = get_html_by_etree(url, headers)
    stringcontent =  selector.xpath('//*[@id="1"]/div/div[1]/div/div[2]/div/text()')
    code = getCode(stringcontent) 
    return code
if __name__ == '__main__':
    url = 'https://www.baidu.com/s?wd={0}&rsv_spt=1&rsv_iqid=0xc37d407f00081027&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&rqlang=cn&tn=baiduhome_pg&rsv_enter=0&rsv_t=03cfHZU83Ou%2B%2FHk%2BN85H%2Ff8qOpekvcm3J9XwKlc3YCtsDeZm62imPhu6Rnuw%2BWN9qj6V&oq=%25E5%25AD%259D%25E6%2584%259F%25E5%25B8%2582%25E9%2582%25AE%25E7%25BC%2596&inputT=936&rsv_pq=ea56053500046b56&rsv_n=2&rsv_sug3=22&bs=%E5%AD%9D%E6%84%9F%E5%B8%82%E9%82%AE%E7%BC%96'
    
    headers = {

        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }
    #selector = get_html_by_etree(url, headers)
    #stringcontent =  selector.xpath('//*[@id="1"]/div/div[1]/div/div[2]/div/text()')
    #contentCode = getCode(stringcontent)
    title = ['地区','原始邮编','百度查询邮编']
    strlines = []
    f = open("./eara.txt",'r')
    contentlist = []
    for line in f.readlines():
        line  = line.split("\n")[0].split('\t')
        contentlist.append(line)
    result = []
    for c in contentlist:
        try:
            tmplist=[]
            quyu = c[1] + '邮编'
            requstUrl = url.format(quyu.strip())
            code =  start(requstUrl,headers)    
            tmplist.append(c[1])
            tmplist.append(int(c[0]))
            tmplist.append(code)
            if int(c[0]) != code :
                print('please check:%s' % (quyu))
            result.append(tmplist)            
        except:
            print("error in get :%s" %(c[1]))
      
    result.sort(key=lambda x:x[0])
    with open('./result.txt','a+',encoding='utf-8') as outputfile:
        outputfile.write((','.join([str(i) for i in title])) +'\n')
        for r in result:
            content = ','.join([str(i) for i in r])
            outputfile.write(content+'\n')    