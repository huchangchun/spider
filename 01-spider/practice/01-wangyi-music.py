# -*- coding:utf-8 -*-
"""
1.抓取所有的分类的id,然后拼接出对应的分类的链接
2.访问分类的链接，抓取所有歌单(专辑)的详细页面的链接
3.访问详细页面的链接，抓取所有歌曲的详细页面的链接
4.抓取歌曲的信息(歌名，歌手名，分类信息）,存储到文本csv或者txt等）或数据库里
5.将歌曲名传递给download_music实现，下载对应音乐文件(这个操作可以只下载一首)
"""
"""
分析：
        1、入口：http://music.163.com/discover/playlist/
        2、每页每个播放列表入口："baseurl+ //div[@class='u-cover u-cover-1']/a/@href"
        3、每个列表中的歌曲：//ul[@class='f-hide']/li/a/@href"
        4、获取下一页入口："//div[@class='u-page']/a[last()]/@href"
                判断是否还有下一页：//div[@class='u-page']/a[last()]/@class")[0] == zbtn znxt
http://music.163.com/song/media/outer/url?id={}.mp3
"""


import requests
from bs4 import BeautifulSoup
from lxml import etree
import time
#获取etree
def get_html_by_etree(url,headers):
    return etree.HTML(requests.get(url,headers=headers).content.decode('utf-8'))


#1.获取所有页面的播放列表入口
def get_play_list(playlisturl,headers,baseurl):
    selector = get_html_by_etree(playlisturl,headers)
    num = 0
    page = 1
    next_page_url = playlisturl
    while True:
        print("这是第{0}页 Url:{1} ".format(page,next_page_url))
        play_list  =[baseurl + i for i in selector.xpath("//div[@class='u-cover u-cover-1']/a/@href")]
        num += len(play_list)
        yield play_list
        time.sleep(0.2)
        next_page_text = selector.xpath("//div[@class='u-page']/a[last()]/@class")[0]
        #判断是否还有下一页
        if next_page_text =='zbtn znxt':
            page += 1
            next_page_url = baseurl + selector.xpath("//div[@class='u-page']/a[last()]/@href")[0]
            selector = get_html_by_etree(next_page_url,headers)
            time.sleep(0.2)
        else:
            break;
    print("总共{0}个playlist ".format(num))

def getsongslist(playlisturl,headers,baseurl):
    num = 0
    for playlists in get_play_list(playlisturl,headers,baseurl):
        for playlist in playlists:
            print("playlist",playlist)
            time.sleep(0.2)
            selector = get_html_by_etree(playlist, headers)
            songurls = selector.xpath("//ul[@class='f-hide']/li/a/@href")
            songurls = [baseurl + i for i in songurls]
            # print("songurls",songurls)
            num  += len(songurls)
            yield  songurls
    print("总共{0}首歌 ".format(num))
def savesongurl(playlisturl,headers,baseurl):
    num = 0
    for songlists in getsongslist(playlisturl,headers,baseurl):
        for songurl in songlists:
            time.sleep(0.2)
            num += 1
            print("获取第{0}首歌信息".format(num))
            songinfo = get_songs_info(songurl,headers)
            save_data(songinfo)
# def get_songs_list(playlisturls,headers,baseurl):
#     songs_list = []
#     num = 0
#     for listurl in playlisturls:
#         num +=1
#         # print("第{0}歌曲列表 ".format(num))
#         selector = get_html_by_etree(listurl, headers)
#         songurls = selector.xpath("//ul[@class='f-hide']/li/a/@href")
#         songs_list += [baseurl + i for i in songurls]
#         # for url in songurls:
#         #     if url not in songs_list:
#         #         songs_list += url
#     print(len(songs_list))
#     print("总共{0}首歌 ".format(len(songs_list)))
#     for i in songs_list:
#         with open('songsurl.txt', 'a+', encoding='utf-8') as outputfile:
#             outputfile.write(i + '\n')
#     return songs_list



#1.获取所有页面的播放列表入口
# def get_play_list(playlisturl,headers,baseurl):
#     selector = get_html_by_etree(playlisturl,headers)
#     play_list =[]
#     page = 1
#     next_page_url = playlisturl
#     while True:
#         print("这是第{0}页 Url:{1} ".format(page,next_page_url))
#         play_list +=[baseurl + i for i in selector.xpath("//div[@class='u-cover u-cover-1']/a/@href")]
#         next_page_text = selector.xpath("//div[@class='u-page']/a[last()]/@class")[0]
#         #判断是否还有下一页
#         if next_page_text =='zbtn znxt':
#             page += 1
#             next_page_url = baseurl + selector.xpath("//div[@class='u-page']/a[last()]/@href")[0]
#             selector = get_html_by_etree(next_page_url,headers)
#         else:
#             break;
#     print("总共{0}个playlist ".format(len(play_list)))
#     # print(play_list)
#     return play_list

#2.获取每页的歌曲
# def get_songs_list(playlisturls,headers,baseurl):
#     songs_list = []
#     num = 0
#     for listurl in playlisturls:
#         num +=1
#         # print("第{0}歌曲列表 ".format(num))
#         selector = get_html_by_etree(listurl, headers)
#         songurls = selector.xpath("//ul[@class='f-hide']/li/a/@href")
#         songs_list += [baseurl + i for i in songurls]
#         # for url in songurls:
#         #     if url not in songs_list:
#         #         songs_list += url
#     print(len(songs_list))
#     print("总共{0}首歌 ".format(len(songs_list)))
#     for i in songs_list:
#         with open('songsurl.txt', 'a+', encoding='utf-8') as outputfile:
#             outputfile.write(i + '\n')
#     return songs_list
#3.获取歌曲详细信息
def get_songs_info(songurl,headers):
    songs_info={}
    time.sleep(0.2)
    selector = get_html_by_etree(songurl, headers)
    songs_info['songname'] = selector.xpath("//em[@class='f-ff2']/text()")[0]
    songs_info['musician'] = selector.xpath("//p[@class='des s-fc4']/span/@title")[0]
    songs_info['cnt_comment_count'] = selector.xpath("string(//span[@class='sub s-fc3']/span)")
    songs_info['songurl'] = songurl
    return songs_info
#保存数据
first_time=True
def save_data(data):
    global  first_time
    if  first_time == True:
        first_time = False
        title =','.join([str(i) for i in data.keys()])
        with open('musics.txt', 'a+', encoding='utf-8') as outputfile:
            outputfile.write(title + '\n')

    content =','.join([str(i) for i in data.values()])
    with open('musics.txt','a+',encoding='utf-8') as outputfile:
        outputfile.write(content+'\n')
if __name__ == '__main__':
    baseUrl = 'http://music.163.com'
    playListUrl = 'http://music.163.com/discover/playlist'
    headers = {

        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'music.163.com',
        'Referer': 'http://music.163.com/search/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
    }

    #获取所有歌单
    # play_lists = get_play_list(playListUrl,headers,baseUrl)
    #获取所有歌曲
    # songurls = get_songs_list(play_lists,headers,baseUrl)
    #获取详细信息
    # data = get_songs_info(songurls[-20:-1],headers)
    # save_data(data)

    savesongurl(playListUrl, headers, baseUrl)
    # url2 = "http://music.163.com/playlist?id=2151717076"
    #
    # url2 = "http://music.163.com/playlist?id=2158379247"
    # re = requests.get(url,headers=headers).content.decode('UTF-8')
    # html = etree.HTML(re)
    # print(html.xpath("//div[@class='u-cover u-cover-1']/a/@href"))
    # print(html.xpath("//div[@class='u-page']/a[last()]/@href")[0])
    # print(html.xpath("//div[@class='u-page']/a[last()]/@class")[0])
    # re2 = requests.get(url2,headers=headers).content.decode('UTF-8')
    # html2 = etree.HTML(re2)
    # with open('wangyi.html', 'a+', encoding='utf-8') as outputfile:
    #     outputfile.write(re2 + '\n')
    # print(html.xpath("//div[@class='ttc']/span/a/@href"))
    # print(html.xpath("//div[@class='ttc']/span/a/b/@title"))
    # print(html.xpath("//div[@class='hd']/span/@data-res-id"))
    # print(html2.xpath("//ul[@class='f-hide']/li/a/@href"))

    # url3="http://music.163.com/song?id=544056874"
    # re3 = requests.get(url3,headers=headers).content.decode('utf-8')
    # html2 = etree.HTML(re3)
    # print(re3)

    # # print(html2.xpath("//p[@class='des s-fc4]/span/@title"))
    # # with open('song.html', 'a+', encoding='utf-8') as outputfile:
    # #     outputfile.write(re3 + '\n')
    # # < div
    # # class ="tit" >
    # # < em
    # # class ="f-ff2" > Double Down < / em >
    # # < / div >
    # # < / div >
    # # < p class ="des s-fc4" > 歌手： < span title="Dave Thomas Junior" > < a class ="s-fc7" href="/artist?id=32233" > Dave Thomas Junior < / a > < / span > < / p >
    # # < p
    # # class ="des s-fc4" > 所属专辑： < a href="/album?id=37763783" class ="s-fc7" > Double Down < / a > < / p >
    # # < div
    # # class ="m-info" >
    # #songname
    # print(html2.xpath("//em[@class='f-ff2']/text()")[0])
    #musician
    # print(html2.xpath("//p[@class='des s-fc4']/span/@title")[0])
    # #span id="cnt_comment_count"
    # print(html2.xpath("string(//span[@class='sub s-fc3']/span)"))


