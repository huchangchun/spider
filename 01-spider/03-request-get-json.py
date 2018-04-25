# -*- coding:utf-8 -*-
import requests
#json响应内容
#requests中有一个内置的json解码器，助理json数据
# re = requests.get("https://github.com/timeline.json")
# print(re.text)
# print(type(re))
# print(re.json())

#GET请求获取原始响应内容
# re = requests.get("https://github.com/timeline.json",stream=True)
# print(re.raw.read(100))

#下载音乐
url="http://m10.music.126.net/20180407111016/abb4af30aaad714386cee6d69c900394/ymusic/7972/9bd1/64cf/f09b5dd5243a059eb8c965ace6acfd21.mp3"
# url = 'http://m10.music.126.net/20180325122236/8cd6773749aede064db8487a2d4b04c8/ymusic/bf31/3157/9c6c/70a1d713578097c8dc54de85e79f2a57.mp3'
re = requests.get(url=url,stream=True)
with open('ka.mp3','wb') as file:
    for chunk in re.iter_content(1024*10):
        file.write(chunk)


