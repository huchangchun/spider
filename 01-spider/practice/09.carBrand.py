#encoding=utf-8
from lxml import etree
import requests
from bs4 import BeautifulSoup
import re
import time
import urllib.request
import re
import zlib
import chardet
import urllib.error
from bs4 import BeautifulSoup
from urllib.parse import quote
import string
from sklearn.externals import joblib
save_path = "./carBrands"
"""
获取太平洋汽车中的汽车品牌

分析：
F12点击平牌树，然后查看sources/index,分析得出平牌是动态返回的：https://price.pcauto.com.cn/index/js/5_5/treedata-cn-7401.js?t=6
需要替换7401到其它平台
1.入口： https://price.pcauto.com.cn/price/nb1/
2.所有品牌：//ul[@class='tree']/li[@class='closeChild']
3.品牌title://ul[@class='tree']/li[@class='closeChild']/a[@class='ppLink'] 
4.品牌herf://ul[@class='tree']/li[@class='closeChild']/a[@class='ppLink'] 
5.品牌列表：https://price.pcauto.com.cn/index/js/5_5/treedata-cn-7401.js?t=6
6. 子品牌品牌名：bt.xpath("//li[@class='banTit']/a/@title")
7. 车名：bt.xpath("//@title")
"""
def getProxyIP(user='my', passwd='xigua'):
    """
    return proxy:
    proxy = {"http":'xigua:Abc123456!@121.43.19.34:8899'}  
    """
    option_proxy = {"http":'xigua:Abc123456!@121.43.19.34:8899'}
    import json
    import requests

    url = 'http://proxycenter.xiguaji.com:8999/Home/GetProxyIp?type=5&isWaited=true'
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
    }

    try:
        response = None
        deadtimes = 0
        while response is None:
            deadtimes += 1
            response = requests.request("get", url, timeout=5)
            if deadtimes == 5 or response:
                break
        if response is None:
            return option_proxy
        return {"http":'{}:{}@{}'.format(user,passwd,response.text)}
    except Exception as ex:
        print(ex)
        return option_proxy

def geturlcontent(url,timelimit=2,  proxy=None, headers=None):
    try:

        context = ''
        proxy = getProxyIP()
        #print("using proxy: ", proxy)
        antuProxy_handler = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(antuProxy_handler)
        url = quote(url,safe=string.printable)
        #请求一定要加headers，不加的异常:requests.exceptions.ConnectionError: ('Connection aborted.', TimeoutError(10060, '由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败。', None, 10060, None))
        reqResponse = urllib.request.Request(url, headers=headers)
        response = opener.open(reqResponse, timeout=timelimit)
      
        if response.getcode() != 404 and response.getcode() != 403 and response.getcode() != 521:
            #获取是否是压缩文件
            info = response.info().get("Content-Encoding")
            htmlbytes = response.read()
            html = ""
            #解压压缩文件
            if info:
                html = zlib.decompress(htmlbytes, 16+zlib.MAX_WBITS)
            else:
                html = htmlbytes
            #得到编码格式
            charsets = chardet.detect(htmlbytes)
            charset = charsets["encoding"]
            response.close()
            if charset == 'GB2312':
                context = html.decode('gb2312', errors='ignore').encode('utf-8').decode('utf-8')
                return context
            else:
                context = html.decode("utf-8")
                return context
        else:
            response.close()
            return context
    except Exception as e:
        return ""
    finally:
        pass

def getProxy():
    proxystr = "121.43.19.34:8899:xigua:Abc123456!"
    proxyInfos = proxystr.split(":")
    proxy = "http://{user}:{pwd}@{ip}:{port}/".format(user=proxyInfos[-2],pwd=proxyInfos[-1], ip=proxyInfos[0], port=proxyInfos[1])
    proxies = {
        "http": proxy
    }       
    return proxies
#获取etree
def get_html_by_etree1(url,headers=None):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36", "Referer":"https://price.pcauto.com.cn/"}

    urlContent = geturlcontent(url)
    if len(urlContent) == 0:
        print("this is a bad entry")
        urlContent = ''
    return urlContent, etree.HTML(urlContent)

def get_html_by_etree(url,headers=None):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36", "Referer":"https://price.pcauto.com.cn/"} 
    proxies = getProxy()
    urlContent = ''
    req = requests.get(url, headers=headers, proxies=proxies)
    encodings = None
    encodings = requests.utils.get_encodings_from_content(req.text)
    if encodings:
        print(encodings)
        urlContent = req.content.decode(encodings[0])
    else:
        urlContent = req.content.decode("gb2312")
         
    return urlContent, etree.HTML(urlContent)


def getIndex(baseUrl):
       
    html, selector = get_html_by_etree(baseUrl)
    brandReg = re.compile('("pictree_\S+")')
    content = re.findall(brandReg, html)
    content = list(set(content))
    
    brandidToReg = re.compile('<a href="/price/q-d[\S\s]+?a>')
    content = re.findall(brandidToReg, html)
    id2Brand = {}
    for i in range(len(content)):
        curTag = content[i]
        selectorTag = etree.HTML(curTag)
        idStr = re.sub("[^(0-9)]","",selectorTag.xpath("//@href")[0])
        brandName = selectorTag.xpath("//text()")[0]
        if idStr not in id2Brand:
            
            id2Brand[idStr] = brandName
        else:
            if id2Brand[idStr] != brandName:
                print("it is impossible")
            print("{} already include: {}".format(idStr, id2Brand[idStr]))
     
    return  id2Brand
def getBrandList(id2Brand):
    indexUrl = "https://price.pcauto.com.cn/index/js/5_5/treedata-cn-{}.js?t=6"
    brand2Product = {}
    brand2Company = {}
    company2Product = {}
    for index, brandName in id2Brand.items():
        dstUrl = indexUrl.format(index)
        
        html,_ = get_html_by_etree(dstUrl)
        if len(html) == 0:
            continue
        selector = etree.HTML(" ".join(re.findall("<li[\s\S]+?</li>", html)))
        subCompanyBrand = selector.xpath("//li[@class='banTit']/a/@title")
        brand2Company[brandName] = subCompanyBrand
        curbrandlist =  selector.xpath("//@title")
        curtotalBrands = selector.xpath("//li[@class='product']/a/@title")
        companyidx = []
        for company in subCompanyBrand:
            companyidx.append(curbrandlist.index(company))
        if len(companyidx) == 1:
            company2Product[company] = curbrandlist[companyidx[0]+1: ]
        else:
            
            for i in range(len(companyidx)):
                if i == len(companyidx) - 1:
                    company2Product[subCompanyBrand[i]] = curbrandlist[companyidx[i]+1: ]
                else:
                    company2Product[subCompanyBrand[i]] = curbrandlist[companyidx[i]+1: companyidx[i+1]]
        assert len(curbrandlist) == (len(subCompanyBrand) + sum([len(company2Product[com]) for com in subCompanyBrand]))
        brand2Product[brandName] = curtotalBrands
    return brand2Product, brand2Company,company2Product

def runGetBrandList():
    baseUrl = 'https://price.pcauto.com.cn'
    id2Brand = getIndex(baseUrl)
    brand2Product, brand2Company,company2Product =  getBrandList(id2Brand)
    joblib.dump([brand2Product, brand2Company,company2Product],save_path)

    print("品牌公司数量：",len(brand2Product))
    print("品牌合资企业数量：",len(company2Product))
    print("汽车品牌数量：",sum([len(product) for brand2,product in brand2Product.items()]))
    print("finnish")
    
    
if __name__=="__main__":
   
    import os
    if  os.path.exists(save_path):
        brand2Product, brand2Company,company2Product = joblib.load(save_path)
        print("品牌公司数量：",len(brand2Company))
        print("品牌合资企业数量：",len(company2Product))
        print("汽车品牌版本数量：",sum([len(product) for brand2,product in brand2Product.items()]))
        print("汽车品牌总数：{}\n".format(len(brand2Product)))
        for i, brand in enumerate(list(brand2Product.keys())):
            if (i+1) % 20== 0:
                print("\n")
            print(brand,end=',')
        print("\n")
        print("奥迪合资企业：\n", brand2Company['奥迪'])    
        print("奥迪品牌：\n", brand2Product['奥迪'])        
       
    else:
        runGetBrandList()