# -*- coding:utf-8 -*-
from lxml import etree
# html = etree.HTML(open('baidu.html',encoding='UTF-8').read())
# result = etree.tostring(html,pretty_print=True,encoding='UTF-8').decode('UTF-8')
# print(result)
html="""
    <!DOCTYPE html>
    <html>
        <head lang="en">
        <title>测试</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        </head>
        <body>
            <div id="content">
                <ul id="ul">
                    <li>NO.1</li>
                    <li>NO.2</li>
                    <li>NO.3</li>                
                    <li>NO.4</li>          
                    <li>NO.5</li>
                </ul>
                <ul id="ul2">
                    <li>one</li>
                    <li>two</li>
                </ul>
                <p class="dec">
                <a title="「你好温柔 让人一瞬间想拿一生来深拥」" href="/playlist?id=2164995466" class="tit f-thide s-fc0">「你好温柔 让人一瞬间想拿一生来深拥」</a>
                </p>
            </div>
            <div id="url">
                <a href="http:www.58.com" title="58">58</a>
                <a href="http:www.csdn.net" title="CSDN">CSDN</a>
            </div>
        </body>
    </html>
"""

selector = etree.HTML(html)
# print(selector.xpath("//div[@id='content']/p/a/@href"))
##这里使用id属性来定位哪个div和ul被匹配 使用text()获取文本内容
content = selector.xpath('//div[@id="content"]/ul[@id="ul2"]/li/text()')
# print(selector.xpath("string(//div[@id='url']/a[2]/text())"))
# print(selector.xpath("string(//div[@id='url'])"))
# print(selector.xpath("string(//div[@id='content']/ul[@id='ul'])"))

# print(content)
# ['one', 'two']
#获取第1个li
# print(selector.xpath("//div[@id='content']/ul[@id='ul2']/li[1]/text()"))
# ['one']
#获取最后一个
# print(selector.xpath("//div[@id='content']/ul[@id='ul']/li[last()]/text()"))
# ['NO.5']
#获取倒数第二个
# print(selector.xpath("//div[@id='content']/ul[@id='ul']/li[last()-2]/text()"))
# ['NO.3']
# print(selector.xpath("//div[@id='content']/ul[@id='ul']/li[position()<4]/text()"))
# ['NO.1', 'NO.2', 'NO.3']

#使用//从全文中定位符合条件的a标签，使用“@标签属性“获取a标签的href属性值
con = selector.xpath('//a/@href')
# print(con)
# ['http:www.58.com', 'http:www.csdn.net']

# print(selector.xpath("string(//div[@id='url']/a[2]/text())"))

#使用绝对路径定位a标签的title
con = selector.xpath('/html/body/div/a/@title')
# print(con)
['58', 'CSDN']
#使用相对路劲定位两者效果一致
con = selector.xpath('//a/@title')
# print(con)
# ['58', 'CSDN']

from lxml import etree
html="""
    <body>
        <div id="aa">aa</div>
        <div id="ab">ab</div>
        <div id="ac">ac</div>
    </body>
    """
selector=etree.HTML(html)
content=selector.xpath('//div[starts-with(@id,"a")]/text()') #这里使用starts-with方法提取div的id标签属性值开头为a的div标签
# for each in content:
#     print(each)

#string(.)标签套标签
html="""
    <div id="a">
    left
        <span id="b">
        right
            <ul>
            up
                <li>down</li>
            </ul>
        east
        </span>
        west
    </div>
"""
sel = etree.HTML(html)
con=sel.xpath("//div[@id='a']/text()")
# for i in con:
#     print(i)
data= sel.xpath("//div[@id='a']")[0]
info = data.xpath('string(.)')
# print(content)
# content = info.replace('\n','').replace(' ','')
# for i in content:
#     print(i)

text = '''<html>

    <div class="large" id="content">

        <span>A line of text</span><br/>  
        <span>B line of text</span><br/>     
        <span>C line of text</span><br/>

        <span><a href="http://google.com">A link</a></span>
        <span><a href="http://baidu.com">B link</a></span>
        <span><a href="http://sougou.com">C link</a></span>
    </div>

    <div class="short" id="footer">

    </div>
</html>
'''

html = etree.HTML(text)
#提取class属性为large的div标签中的id属性值
print(html.xpath("//div[@class='large']/@id"))
# ['content']
print(html.xpath("//div[@class='large']/@id")[0])
# content
#提取第一个span标签中的文本信息
print(html.xpath("//span/text()"))
# ['A line of text', 'B line of text', 'C line of text']
print(html.xpath("//span/text()")[0])
# A line of text
#提取第二个span标签中的链接
print(html.xpath("//span/a/@href"))
#['http://google.com', 'http://baidu.com', 'http://sougou.com']
print(html.xpath("//span/a/@href")[0])
# http://google.com