# -*- coding:utf-8 -*-
from lxml import etree
import requests
from bs4 import BeautifulSoup
import re
import time
"""
获取智联招聘信息

分析：
    1、入口：http://sou.zhaopin.com
    2、所有职位url://div[@id='search_right_demo']/div/div/a
    3、获取详细职位列表的url://td[@class='zwmc']/div/a[1]
        下一页：//a[@class='next-page']
    4、获取职位详细信息
        zwmc://div[@class='fl']/h1
        gsmc://div[@class='fl']/h2
        gsfl://div[@class='fl' or @class='inner-left fl']/div/span/text()
            ://div[@class='terminalpage-left']/ul/li[1]
            
"""
#1.获取所有职位分类列表
def get_job_cat_list(url,headers):
    r = requests.get(url,headers=headers).content.decode('utf-8')
    # print(r)
    html = etree.HTML(r)
    job_list = html.xpath("//div[@id='search_right_demo']/div/div/a/@href")
    pattern = re.compile('jl=\d+&')
    #jl=489表示全国
    job_list = [url[:-1] + str(pattern.sub('jl=489&',i)) for i in job_list]
    # print(job_list)
    return job_list

#2获取职位列表
def get_job_list(url,headers):
    r = requests.get(url,headers=headers).content.decode('utf-8')
    html = etree.HTML(r)
    job_list = html.xpath("//td[@class='zwmc']/div/a[1]/@href")
    next_page = html.xpath("//a[@class='next-page']/@href")
    # print(next_page)
    return job_list ,next_page

#3.获取职位详细信息
def get_job_info(url,headers):
    zwlis =[]
    def clean_none(data):
        if data['zwmc'] == '' or data['zwmc'] in zwlis:
            return False
        else:
            zwlis.append(data['zwmc'])
            data['zwmc'] = '_'.join(data['zwmc'])
            return data

    #清洗数据
    def clear_data(data):
        #gsfl
        data['gsfl'] = '_'.join(data['gsfl'])
        #zwyx
        pattern = re.compile('\d+')
        zwyx = pattern.findall(data['zwyx'])
        if len(zwyx) == 2:
            data['min_zwyx'] = zwyx[0]
            data['max_zwyx'] = zwyx[1]
        else:
            data['min_zwyx'] = data['max_zwyx'] = data['zwyx']
        data.pop('zwyx')
        #zprs
        data['zprs'] = data['zprs'].strip('人 ')
        #gzdd
        data['gzdd'] = data['gzdd'].split('-')[0]
        return data


    r = requests.get(url,headers=headers).content.decode('utf-8')
    html = etree.HTML(r)
    job_dic = {}
    #获取详细信息
    #工作名称
    job_dic['zwmc'] = html.xpath("string(//div[@class='fl' or @class='inner-left fl']/h1)")
    # 公司名称
    job_dic['gsmc'] = html.xpath("string(//div[@class='fl' or @class='inner-left fl']/h2)")
    #公司福利
    job_dic['gsfl'] = html.xpath("//div[@class='fl' or @class='inner-left fl']/div/span/text()")
    #职位月薪
    job_dic['zwyx'] = html.xpath("string(//div[@class='terminalpage-left']/ul/li[1]/strong)")
    #工作地点
    job_dic['gzdd'] = html.xpath("string(//div[@class='terminalpage-left']/ul/li[2]/strong)")
    #发布日期
    job_dic['fbrq'] = html.xpath("string(//div[@class='terminalpage-left']/ul/li[3]/strong)")
    # 工作性质
    job_dic['gzxz'] = html.xpath("string(//div[@class='terminalpage-left']/ul/li[4]/strong)")
    #工作经验
    job_dic['gzjy'] = html.xpath("string(//div[@class='terminalpage-left']/ul/li[5]/strong)")
    # 最低学历
    job_dic['zdxl'] = html.xpath("string(//div[@class='terminalpage-left']/ul/li[6]/strong)")
    #招聘人数
    job_dic['zprs'] = html.xpath("string(//div[@class='terminalpage-left']/ul/li[7]/strong)")
    #职位类别
    job_dic['zwlb'] = html.xpath("string(//div[@class='terminalpage-left']/ul/li[8]/strong)")

    jobdata = clean_none(job_dic)

    if jobdata:
        jobdata = clear_data(jobdata)
        save_data(jobdata)

#保存数据
first_time=True
def save_data(data):
    global  first_time
    if  first_time == True:
        first_time = False
        title =','.join([str(i) for i in data.keys()])
        with open('zhilian-job.txt', 'a+', encoding='utf-8') as outputfile:
            outputfile.write(title + '\n')

    content =','.join([str(i) for i in data.values()])
    with open('zhilian-job.txt','a+',encoding='utf-8') as outputfile:
        outputfile.write(content+'\n')
if __name__=='__main__':
    url= 'http://sou.zhaopin.com/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    #1 获取所有职位分类列表
    urlist = get_job_cat_list(url,headers)

    #2.获取详细职位信息
    page = 0
    hangye = 0
    total = 0
    for subEntry in urlist:
        hangye +=1
        num = 0
        page +=1
        job_list, next_page = get_job_list(subEntry,headers)
        for job_url in job_list:
            num+= 1
            total += 1
            print("第{}个行业第{}页第{}个职位.总共是第{}个职位".format(hangye, page, num,total))
            get_job_info(job_url, headers)
            # time.sleep(0.02)
        #每一个行业有多个页面的职位
        while next_page:
            page +=1
            num = 0
            job_list, next_page = get_job_list(next_page[0], headers)
            for job_url in job_list:
                num += 1
                total += 1
                print("第{}个行业第{}页第{}个职位.总共是第{}个职位".format(hangye, page, num, total))
                get_job_info(job_url, headers)
                # time.sleep(0.02)