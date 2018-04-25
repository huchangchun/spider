# -*- coding:utf-8 -*-
import urllib.request as urlrequest
from bs4 import BeautifulSoup
top250_url ='https://movie.douban.com/top250?start={}&filter='
with open('top205_f1.csv','w+',encoding='utf8') as outputfile:
    outputfile.write('num#title#director#role#init_year#area#genre#rating_num#comment_num#comment#url\n')
    all_item_divs = None
    for  i in range(2):
        start = i *25
        url_visit = top250_url.format(start)
        # print(url_visit)
        crawl_content = urlrequest.urlopen(url_visit).read().decode('utf8')
        # print(crawl_content)
        soup = BeautifulSoup(crawl_content,'html.parser')
        all_item_divs = soup.find_all(class_='item')
        # print(all_item_divs)
        # print(all_item_divs[0])
        for each_item_div in all_item_divs:
            pic_div = each_item_div.find(class_='pic')
            num = pic_div.find('em').get_text() #排名
            href = pic_div.find('a')['href'] #电影连接
            title = pic_div.find('img')['alt']  #电影名称
            bd_div = each_item_div.find(class_='bd')
            infos = bd_div.find('p').get_text().strip().split('\n')
            infos_1 = infos[0].split('\xa0\xa0\xa0')
            director = infos_1[0][4:].rstrip('...').rstrip('/').split('/')[0] # 导演
            role = str(infos_1[1:])[6:].split('/')[0]
            infos_2 = infos[1].lstrip().split('\xa0/\xa0')
            year = infos_2[0]
            area = infos_2[1]
            genre = infos_2[2:]
            # print(each_item_div)
            star_div = each_item_div.find(class_='star')
            rating_num = star_div.find(class_='rating_num').get_text() #评分
            comment_num = star_div.find_all('span')[3].get_text()[:-3]
            quote = each_item_div.find(class_='quote')
            inq = quote.find(class_='inq').get_text() #一句话评价
            outputfile.write('{}#{}#{}#{}#{}#{}#{}#{}#{}#{}#{}#\n'.format(
                num,title,director,role,
                year,genre,area,rating_num,
                comment_num,inq,href
            ))