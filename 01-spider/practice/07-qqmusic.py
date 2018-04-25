# -*- coding:utf-8 -*-

"""
步骤
    一、选择歌单

    二、选择歌曲

    三、播放音乐


下载音乐
    meida:
    http://dl.stream.qqmusic.qq.com/C4000037HlEP0subhS.m4a?vkey=E84B6522C515D0E67E0D28FC2C67A99EAFEACD80C604554C9F2148B37C60B032CF427AD5E1CE946BEF180B0E3729E90430736FE55C7D77F1&guid=1093240106&uin=0&fromtag=66

    需要参数：
    vkey: E84B6522C515D0E67E0D28FC2C67A99EAFEACD80C604554C9F2148B37C60B032CF427AD5E1CE946BEF180B0E3729E90430736FE55C7D77F1
          E84B6522C515D0E67E0D28FC2C67A99EAFEACD80C604554C9F2148B37C60B032CF427AD5E1CE946BEF180B0E3729E90430736FE55C7D77F1

    标识符： 0037HlEP0subhS
    songmid:"C400"+"0037HlEP0subhS"+".m4a"


二、如何获取 songmid  vkey
url:
    https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg?g_tk=5381&jsonpCallback=MusicJsonCallback07572169456335454&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361747&callback=MusicJsonCallback07572169456335454&uin=0&songmid=0037HlEP0subhS&filename=C4000037HlEP0subhS.m4a&guid=1093240106

可以返回：
    songmid
    vkey


需要参数：

    songmid: 0037HlEP0subhS
    filename: C4000037HlEP0subhS.m4a


    songmid: 0037Agik13imJS
    filename: C4000037Agik13imJS.m4a


三、继续查找songmid
url：
    https://c.y.qq.com/qzone/fcg-bin/fcg_ucc_getcdinfo_byids_cp.fcg?type=1&json=1&utf8=1&onlysong=0&disstid=3806226626&format=jsonp&g_tk=5381&jsonpCallback=playlistinfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0

返回：
    songmid
    songname


需要参数：
disstid: 3806226626

四、查找disstid
url：
    https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?picmid=1&rnd=0.34692207151847465&g_tk=5381&jsonpCallback=getPlaylist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&categoryId=10000000&sortId=5&sin=0&ein=29

返回：
    dissid 列表

需要参数
    sin: 0
    ein: 29

"""

import requests
import  json
if __name__ == '__main__':
    start_url = 'https://c.y.qq.com/splcloud/fcgi-bin/fcg_get_diss_by_tag.fcg?picmid=1&rnd=0.34692207151847465&g_tk=5381&jsonpCallback=getPlaylist&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&categoryId=10000000&sortId=5&sin={0}&ein={1}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
        'Referer':'https://y.qq.com/portal/player.html'
    }
    sin= 0
    ein = 29
    while True:
        res = requests.get(start_url.format(sin,ein),headers = headers).text
        print(res)
        dissid_dic = json.loads(res.strip('getPlaylist()'))
        for item in dissid_dic['data']['list']:
            disstid = item['dissid']
            dissname = item['dissname']
            print(disstid)
            print(dissname)
        #通过dissid获取
        break