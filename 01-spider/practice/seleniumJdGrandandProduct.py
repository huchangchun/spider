#encoding=utf-8
from selenium.webdriver.support import ui
from selenium.webdriver import Chrome
import time,os
from bs4 import BeautifulSoup 
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from lxml import etree
import numpy as np
if os.path.exists("C:\\Users\zxy\AppData\Local\Google\Chrome\Application\chromedriver.exe"):
    driver = Chrome("C:\\Users\zxy\AppData\Local\Google\Chrome\Application\chromedriver.exe")
else:
    driver = Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
"""
环境要求：
1. pip install selenium
2.需要将chromedriver.exe放在driver所指路径，下载时要与本地chrome版本匹配或更新，具体版本查看chrome
下载地址：http://npm.taobao.org/mirrors/chromedriver/

"""
def isNoneOrEmpty(s):
   
    if s is None:
        return True
    if isinstance(s, list):
        
        if len(s) == 0:
            return True
        else:
            return False
        
    if isinstance(s, tuple):
        if len(s) == 0:
            return True
        else:
            return False
        
    if isinstance(s, str):
        if len(s) == 0:
            return True
        else:
            return False
        
    if isinstance(s,dict):
        if len(s) == 0:
            return True
        else:
            return False
        
    if isinstance(s, set):
        if len(s) == 0:
            return True
        else:
            return False
        
    if isinstance(s, int):
        return False

def grabBrands(url):
    goodsname = []
    
    try:
        driver.get(url)
        mulitipchose = "//*[@id='J_selector']/div[1]/div/div[3]/a[2]"
        more = "//*[@id='J_selector']/div[1]/div/div[3]/a[1]"
        cancelBtn = "//*[@id='J_selector']/div[1]/div/div[2]/div[4]/a[2]" 
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, mulitipchose)))        
        element.click()
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, cancelBtn)))  
        page = driver.page_source
        soup = BeautifulSoup(page,'html.parser')
        data1 = soup.find('ul',{"class":"J_valueList v-fixed"})
        datali =data1.find_all('li')    
        for i in datali:
            goodsname.append(i.a.attrs['title'])
        print("品牌数量：", len(goodsname))
        
    except Exception as ex:
        
        # 关闭当前标签，也可以使用quit()关闭浏览器
        
        return None
    return goodsname

def grabGoodsTypeWithClass(url):
    
    goodsname=[]
    goodshref=[]
    
    try:
        brower = webdriver.Chrome() 
        brower.get(url)        
        page = brower.page_source
       
        soup = BeautifulSoup(page,'html.parser')
        dataAll = soup.find_all(attrs={"class":"J_selectorLine s-category"})
        if   isNoneOrEmpty(dataAll):
            return None
        for i in range(len(dataAll)):
            curdata = dataAll[i].find("ul",{"class":"J_valueList"})
            datali = curdata.find_all('li')
            for i in datali:
                goodsname.append(i.a.attrs['title'])
                goodshref.append(i.a.attrs['href'])
                print("当前数量：", len(goodsname))
     
        print(goodsname[:10])
    except Exception as ex:
        print(ex)
    # 关闭当前标签，也可以使用quit()关闭浏览器
        
        return None
    return goodsname, goodshref

def runGrabBrands(goodClass: list, notallowlist=None):
    url = "https://search.jd.com/Search?keyword={}&enc=utf-8"
     
    allgoods = []
    allgoodsBrands=[]
     
    for gcls in goodClass:
        print("大类：", gcls)
        flag = True
        while flag:
            curgoods, _ = grabGoodsTypeWithClass(url.format(gcls))
            if not isNoneOrEmpty(curgoods):
                allgoods.extend(curgoods)
                print("当前总品类数：", len(allgoods))
                flag = False
            else:
                print("{}获取异常,重试".format(gcls))
    print("总品类数：", len(allgoods))
    allgoods = list(set(allgoods))
    allgoods =  [g  for g in allgoods if len(g) > 1]
    print("去重后总品类数：", len(allgoods))
    if notallowlist is not None:
        allgoods = [g for g in allgoods if g not in notallowlist]
    with open("{}.txt".format(",".join(goodClass)), mode='w', encoding='utf-8') as f:
        f.write(",".join(allgoods))
    print("前十个品类：", ",".join(allgoods[:10]))
    for goodtype in allgoods:
        
        print("获取品类品牌：{} ".format(goodtype))
        flag = True
        i= 0
        while flag:
            if  isinstance(goodtype, list):
                curgoodbrand = []
                for gt in goodtype:
                    curgoodbrand.extend(grabBrands(url.format(gt)))
            else:
                curgoodbrand = grabBrands(url.format(goodtype))
            if not isNoneOrEmpty(curgoodbrand):
                print(curgoodbrand)
                allgoodsBrands.extend(curgoodbrand)                       
                print("当前总品牌数量:", len(allgoodsBrands))
                flag = False
            else:
                print("{}获取异常,重试".format(goodtype))
                goodtype = goodtype.split("/")
                i += 1
                if i == 3:
                    print("获取异常,重试{}次失败".format(i))
                    flag = True

    print("总品牌数量:", len(allgoodsBrands))
    print("去重后数量:", len(list(set(allgoodsBrands))))
    if  isNoneOrEmpty(allgoodsBrands):
        print("数据为空")
        return None
    saveData("{}品牌.xlsx".format(",".join(goodClass)),list(set(allgoodsBrands)))
    
def getAliseFromBrand(brand):
    import re
    kuohaopattern = "（(.*)）"
    curalias = re.findall(kuohaopattern, brand)
    curbrand = re.sub(kuohaopattern,"", brand)
    if len(curalias) > 0:
        return curbrand,curalias[0]
    else:
        return curbrand,curbrand
    
def saveData(savefile, data):
    brands, aliass = [],[]
    import re
   
    for b in data:
        aliass.append(getAliseFromBrand(b)[1])
        brands.append(getAliseFromBrand(b)[0])
    assert len(brands) == len(aliass)
    import pandas as pd
    
    df = pd.DataFrame({"Brand": brands,"Alias": aliass})
    df.to_excel(savefile, encoding='utf-8')
    print("finnish")

def readBrandsFromXlsx(filepath, savefile):
    import pandas as pd
    df = pd.read_excel(filepath, encoding='utf-8')
    brands = df['Brand'].tolist()
    aliass = df['Alias'].tolist()
    brandsdic ={}
    for brand, alias in zip (brands, aliass):
        if brand in brandsdic:
            continue
        else:
            brandsdic[brand] = alias
        
   
    df = pd.DataFrame({"Brand": list(brandsdic.keys()),"Alias": list(brandsdic.values())})
    df.to_excel(savefile, encoding='utf-8')
    
    
def testGrabBrand():
    good = '牙膏'
    url = "https://search.jd.com/Search?keyword={}&enc=utf-8" 
    curgoodbrand = grabBrands(url.format(good))
    print(curgoodbrand)
    saveData("{}品牌.xlsx".format(good), curgoodbrand)
 
 
def grabGoodTitlesWithGoodType(url):
    try:
        brower = webdriver.Chrome() 
        brower.get(url)        
        page = brower.page_source
        selector = etree.HTML(page)
        titlespath = "//*[@id='J_goodsList']/ul/li/div/div[3]/a/@title"   
        subtitlespath = "//*[@id='J_goodsList']/ul/li[{}]/div/div[3]/a/em/text()"   
        subtypespath = "//*[@id='J_goodsList']/ul/li[{}]/div/div[3]/a/em/font/text()"   
        totalpagepath ='//*[@id="J_bottomPage"]/span[2]/em[1]/b/text()'
        nextpagebtnpath = '//*[@id="J_bottomPage"]/span[1]/a[9]'
        totalpageCount = int(selector.xpath(totalpagepath)[0])
        if totalpageCount > 13:
            print("超过13页，截断")
            totalpageCount = 13
        titles = []
        def gettitles(slt):
            try:
                
                curtitles = []
                emselectors = slt.xpath(titlespath)
                for i in range(len(emselectors)):    
                    emtypes = slt.xpath(subtypespath.format(i))
                    emtitles = slt.xpath(subtitlespath.format(i))
                    if isinstance(emtypes,list):
                        if len(emtypes) == 0:
                            emtypes =['']
                    if (emtitles) == 0:
                        continue
            
                    curtitle =''
                    emtypes = emtypes[::-1]
                    for i in range(len(emtitles)):
                        curtitle  += emtitles[i]
                        if len(emtypes) > 0:
                            curtitle += emtypes.pop()
                        if len(emtypes) > 0:
                            for i in range(len(emtypes)):
                                curtitle += emtypes.pop()
                    curtitle = "".join(list(set(emtypes))) + "".join(emtitles)
                    if len(curtitle) !=0:
                        curtitles.append(curtitle)
                return curtitles
            except Exception as ex:
                return []
        curtitles = gettitles(selector)
        if len(curtitles) != 0:
            titles.extend(curtitles)
        for  i in range(totalpageCount - 1):
            try:
                brower.find_elements_by_xpath(nextpagebtnpath)[0].click()
                WebDriverWait(brower, 10)#.until(EC.element_to_be_clickable((By.XPATH, nextpagebtnpath)))  
                page = brower.page_source
                selector = etree.HTML(page)
                if len(curtitles) != 0:
                    titles.extend(curtitles) 
            except Exception as ex:
                pass
        print(len(titles))
        print(len(list(set(titles))))
        print(titles)   
        brower.quit()
    except Exception as ex:
        print(ex)
 
    # 关闭当前标签，也可以使用quit()关闭浏览器
        
        return None
    return titles  


def runGrabGoodTitlesWithTypes(goodtypes:dict):
    savetitles = []
    savetypes = []
    url = "https://search.jd.com/Search?keyword={}&enc=utf-8"
    for gt, subgtlist in goodtypes.items():
        for subgt in subgtlist:
            curtitles = grabGoodTitlesWithGoodType(url.format(subgt))
            if len(curtitles) == 0:
                print("类型{} 没有取到数据".format(subgt))
            else:
                savetitles.extend(curtitles)
                savetypes.extend([gt] * len(curtitles))
    import pandas as pd
    df = pd.DataFrame.from_dict({"title":savetitles, "goodtype":savetypes})
    df.to_excel('商品标题分类信息.xlsx')
if __name__=="__main__":
    
    #url = "https://search.jd.com/Search?keyword={}&enc=utf-8"
    #grabGoodTitlesWithGoodType(url.format('花鸟盆栽'))
    runGrabGoodTitlesWithTypes({"花鸟宠物":['宠物衣服','花鸟盆栽','花鸟宠物','宠物零食','宠物生活用品']})
    
    
    #readBrandsFromXlsx("美妆,洗护,护肤,彩妆,口腔洗护品牌.xlsx","美妆,洗护,护肤,彩妆,口腔洗护品牌new.xlsx")
    #testGrabBrand()
    #runGrabBrands(['美妆','洗护','护肤','彩妆','口腔洗护'])
    
    #notallowlist =['宗教用品',
 #'特殊商品',
 #'历史',
 #'礼品文具',
 #'港台图书',
 #'礼品定制',
 #'古董文玩',
 #'婚庆节庆',
 #'创意礼品',
 #'配件',
 #'工艺礼品',
 #'电子礼品',
 #'挂件/摆件/把件',
 #'婚庆饰品',
 #'美妆礼品']
    #runGrabBrands(['花鸟盆栽'])
    #notallowlist=['避孕套',
 #' 充气/仿真娃娃',
 #'辅酶Q10',
 #'仿真阳具',
 #'震动棒',
 #'其他',
 #'飞机杯',
 #' 男用延时',
 #'其他情趣用品',
 #'倒模']
    #runGrabBrands(['保健品','滋补','营养品'])
    #runGrabBrands(['日用百货'])
    #pass  
    