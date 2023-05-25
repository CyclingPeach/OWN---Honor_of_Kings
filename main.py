"""
    Topic:  王者荣耀英雄信息采集及分析
    Time:   2020.12 --- Dec,2020
    Author: 陶志远 --- Zhiyuan Tao
"""

import os
import csv
import time
import requests
from bs4 import BeautifulSoup
import lxml.etree
from selenium import webdriver
import pandas as pd


user_agent = [
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Maxthon 2.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; TencentTraveler 4.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; The World)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SE 2.X MetaSr 1.0; SE 2.X MetaSr 1.0; .NET CLR 2.0.50727; SE 2.X MetaSr 1.0)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser)"
]

# url = 'https://pvp.qq.com/web201605/herolist.shtml'

'''两种不同的网页解析方法'''
'''
    BeautifulSoup + html.parser 解析网页    使用 selector 获取网页数据
'''
def print_one_hero_soup(one_hero_url):
    one_hero_response = requests.get(one_hero_url)
    one_hero_response.encoding = one_hero_response.apparent_encoding    # 获取网页真实编码    https://www.cnblogs.com/bw13/p/6549248.html
    one_hero_html = one_hero_response.text
    one_hero_soup = BeautifulSoup(one_hero_html, 'html.parser')    # BeautifulSoup + html.parser解析器
    
    return one_hero_soup

'''
    selenium + lxml             解析网页    使用 xpath 获取网页源代码某处具体数据
'''
def print_one_hero_xpath(one_hero_url):
  
    options = webdriver.ChromeOptions()                     # 操作 Chrome 浏览器
    options.headless = True                                 # 不弹出 Chrome浏览器界面，后台运行
    driver = webdriver.Chrome(chrome_options = options)     # 控制chrome浏览器
    
    driver.get(one_hero_url)
    time.sleep(2)
    content = driver.page_source            # selenium 获取网页源代码
    cont_xph = lxml.etree.HTML(content)     # 解析 content
    
    return cont_xph

'''
    获取所有英雄的url链接
    注: 可以通过网页 json 文件获取英雄信息, 这样才是正确的方法, 不仅效果好而且速度更快【2022-05-20记, 暂未更新】
'''
def get_all_hero_urls(url):
    
    response = requests.get(url)
    response.encoding = response.apparent_encoding    # 获取网页真实编码'GB2312'
    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    
    selector_str = 'body > div.wrapper > div.zkcontent > div.zk-con-box > div.herolist-box > div.herolist-content > ul.herolist.clearfix > li > a'
    data   = soup.select(selector_str + ' > img')
    data2  = soup.select(selector_str)
    
    hero_name_lists = [] 
    hero_url_lists = []
    herolist_url_herd = 'https://pvp.qq.com/web201605/'
    
    for item in data:
        alt = item.get('alt')
        hero_name_lists.append(alt)
    for item in data2:
        href = herolist_url_herd + item.get('href')
        hero_url_lists.append(href)
    
    # 英雄‘夏侯惇’页面数据编码有问题，这里将其删除
    for i in range(len(hero_name_lists)):
        if '夏侯' in hero_name_lists[i]:
            break
    hero_name_lists.pop(i)
    hero_url_lists.pop(i)
       
    '''
        >>> zip([1,2,5],[3,4,6])
        <zip object at 0x7f9d886b5700>
    
        >>> list(zip([1,2,5],[3,4,6]))
        [(1, 3), (2, 4), (5, 6)]
        
        zip()   函数 返回两个list的各元素一一对应组成的多个元组的对象
        list()  函数 将其转换为 列表
    '''
    return list(zip(hero_name_lists, hero_url_lists))


'''
    英雄基本信息
'''
def get_hero_info(one_hero_soup):
    head_select = 'body > div.wrapper > div.zk-con1.zk-con > div > div > div.cover'
    name = one_hero_soup.select(head_select + ' > h2')[0]
    name = name.get_text()
    
    basic_info = [name]
    for j in one_hero_soup.select(head_select + ' > ul > li > span > i'):
        basic_info.append(j.get('style')[6:])
        
    with open('./王者荣耀英雄基本信息.csv', 'a', encoding='GBK') as file:
        writer = csv.writer(file)
        writer.writerow(basic_info)
def save_hero_info():
    if os.path.isfile('./王者荣耀英雄基本信息.csv') == True:
        os.remove('./王者荣耀英雄基本信息.csv')

    for one_hero_url in get_all_hero_urls(url):
        one_hero_soup = print_one_hero_soup(one_hero_url[1])
        try:
            get_hero_info(one_hero_soup)
        except:
            pass
        continue


'''
    英雄皮肤
'''
def get_hero_clo(hero_name, one_hero_soup):
    clo_selector = 'body > div.wrapper > div.zk-con1.zk-con > div > div > div.pic-pf > ul'
    clos_name_str = one_hero_soup.select(clo_selector)[0].get('data-imgname')
    clo_name_list = clos_name_str.split('|')
    hero_clo_list = [hero_name]
    for name in clo_name_list:
        hero_clo_list.append(name[0:name.find('&')])
    with open('./王者荣耀英雄皮肤.csv', 'a', encoding='GBK') as file:
        writer = csv.writer(file)
        writer.writerow(hero_clo_list)
        
    return hero_clo_list
def save_get_hero_clo():
    if os.path.isfile('./王者荣耀英雄皮肤.csv') == True:
        os.remove('./王者荣耀英雄皮肤.csv')

    for one_hero_url in get_all_hero_urls(url):
        one_hero_name = one_hero_url[0]
        one_hero_soup = print_one_hero_soup(one_hero_url[1])
        try:
            get_hero_clo(one_hero_name, one_hero_soup)
        except:
            pass
        continue


'''
    英雄技能介绍
'''
def get_skills_info(hero_name,cont_xph):   
    head_xpath = '/html/body/div[3]/div[2]/div/div[1]/div[2]/div/div'

    skill_info1 = cont_xph.xpath(head_xpath + '/div/p[1]/b/text()')
    skill_info2 = cont_xph.xpath(head_xpath + '/div/p[2]/text()')
    skill_info = [hero_name] + skill_info1 + skill_info2

    with open('./王者荣耀英雄技能介绍.csv', 'a', encoding='GBK') as file:
        writer = csv.writer(file)
        writer.writerow(skill_info)
        
def save_skills_info():
    if os.path.isfile('./王者荣耀英雄技能介绍.csv') == True:
        os.remove('./王者荣耀英雄技能介绍.csv')
    for one_hero_url in get_all_hero_urls(url):
        hero_name = one_hero_url[0]
        cont_xph  = print_one_hero_xpath(one_hero_url[1])

        try:
            get_skills_info(hero_name, cont_xph)
        except:
            pass
        continue


'''
    英雄铭文搭配推荐
'''
def get_mingwen_sugg(hero_name, cont_xph):
    xpath_herd = '/html/body/div[3]/div[2]/div/div[1]/div[3]/div[2]'
    name_xpath = xpath_herd + '/ul/li/p[1]/em/text()'
    tips       = cont_xph.xpath(xpath_herd + '/p/text()')
    tips = str(tips)[7:-2]
    mingwen    = cont_xph.xpath(name_xpath)
    mingwen_sugg = [hero_name] + mingwen + [tips]
    with open('./王者荣耀铭文搭配推荐.csv', 'a', encoding='GBK') as file:
        writer = csv.writer(file)
        writer.writerow(mingwen_sugg)

def save_mingwen_sugg():
    if os.path.isfile('./王者荣耀铭文搭配推荐.csv') == True:
        os.remove('./王者荣耀铭文搭配推荐.csv')
    for one_hero_url in get_all_hero_urls(url):
        hero_name = one_hero_url[0]
        cont_xph  = print_one_hero_xpath(one_hero_url[1])
        
        try:
            get_mingwen_sugg(hero_name, cont_xph)
        except:
            pass
        continue


'''
    英雄技能加点建议
'''
def get_skill_plus_sugg(hero_name, cont_xph):
    
    head_xpath = '/html/body/div[3]/div[2]/div/div[2]/div[1]/div[@class="sugg-info2 info"]/p/span/text()'
    get_skill_plus_sugg_name  = cont_xph.xpath(head_xpath)

    skill_plus_sugg = [hero_name]
    for plus in range(len(get_skill_plus_sugg_name)):
        skill_plus_sugg.append(get_skill_plus_sugg_name[plus])
        
    with open('./王者荣耀英雄技能加点建议.csv', 'a', encoding='GBK') as file:
        writer = csv.writer(file)
        writer.writerow(skill_plus_sugg)
def save_plus_sugg():
    if os.path.isfile('./王者荣耀英雄技能加点建议.csv') == True:
        os.remove('./王者荣耀英雄技能加点建议.csv')
    for one_hero_url in get_all_hero_urls(url):
        hero_name = one_hero_url[0]
        cont_xph  = print_one_hero_xpath(one_hero_url[1])
        
        try:
            get_skill_plus_sugg(hero_name, cont_xph)
        except:
            pass
        continue


'''
    王者荣耀英雄出装建议
'''
def get_equip_sugg(hero_name, cont_xph):
    for i in range(1,3):
        header_xpath  = '/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/div[' + str(i) + ']/ul/li/a/div'
        tips_xpath    = '/html/body/div[3]/div[2]/div/div[2]/div[2]/div[2]/div[' + str(i) + ']/p'

        JNAME_xpath   = header_xpath + '/div[1]/div/h4'    # 装备名
        JNAME   = cont_xph.xpath(JNAME_xpath  )
        Jtips   = cont_xph.xpath(tips_xpath   )
        Jtip = Jtips[0].xpath('.//text()')
                
        get_equip_sugg = [hero_name]
        if i == 1:
            get_equip_sugg.append(' 一 ')
        if i == 2:
            get_equip_sugg.append(' 二 ')
        
        for xp in JNAME:
            name = xp.xpath('.//text()')[0]
            get_equip_sugg.append(name)
        get_equip_sugg.append(str(Jtip)[7:-2])
        with open('./王者荣耀英雄出装建议.csv', 'a', encoding='GBK') as file:
            writer = csv.writer(file)
            writer.writerow(get_equip_sugg)
def save_equip_sugg():
    if os.path.isfile('./王者荣耀英雄出装建议.csv') == True:
        os.remove('./王者荣耀英雄出装建议.csv')

    for one_hero_url in get_all_hero_urls(url):
        hero_name = one_hero_url[0]
        cont_xph  = print_one_hero_xpath(one_hero_url[1])
        try:
            get_equip_sugg(hero_name, cont_xph)
        except:
            pass
        continue


'''
    王者荣耀英雄关系
'''
def get_relates_list(hero_name, one_hero_soup):
    herolist_url_herd = 'https://pvp.qq.com/web201605/herodetail/'

    for i in range(1, 4):
        selector = 'body > div.wrapper > div.zkcontent > div > div.zk-con4.zk-con > div.hero.ls.fl > div.hero-info-box > div > div:nth-child(' + str(i) + ') > '
        relate = one_hero_soup.select(selector + 'div.hero-f1.fl')[0].get_text()

        names = []
        href_url_lables = one_hero_soup.select(selector + 'div.hero-list.hero-relate-list.fl > ul > li > a')

        for item in href_url_lables:
            href = herolist_url_herd + item.get('href')
            href_response = requests.get(href)
            href_response.encoding = href_response.apparent_encoding
            href_soup = BeautifulSoup(href_response.text)
            name = href_soup.select('body > div.wrapper > div.zk-con1.zk-con > div > div > div.cover > h2')[0].get_text()
            names.append(name)
        effect_1 = one_hero_soup.select(selector + 'div.hero-list-desc > p')[0].get_text()
        effect_2 = one_hero_soup.select(selector + 'div.hero-list-desc > p')[1].get_text()
        
        relates_list_new = [hero_name, relate, names[0], names[1], effect_1, effect_2]
        
        with open('./王者荣耀英雄关系.csv', 'a', encoding='GBK') as file:
            writer = csv.writer(file)
            writer.writerow(relates_list_new)
def save_relates_list():
    if os.path.isfile('./王者荣耀英雄关系.csv') == True:
        os.remove('./王者荣耀英雄关系.csv')

    for one_hero_url in get_all_hero_urls(url):
        hero_name = one_hero_url[0]
        one_hero_soup  = print_one_hero_soup(one_hero_url[1])
        try:
            get_relates_list(hero_name, one_hero_soup)
        except:
            # print(one_hero_url)     # 实际运行后发现有三个英雄出现错误
            pass
        continue

def pretreatment():
    save_hero_info = pd.read_csv('./王者荣耀英雄基本信息.csv',encoding='GBK',names=['英雄名','生成能力','攻击伤害','技能效果','上手难度'])
    # 去空值
    save_hero_info.dropna(axis=0, inplace=True)  # 删除有空值的行，使用参数axis = 0
    save_hero_info.index = range(len(save_hero_info))  # 重新设置列索引
    # print(save_hero_info)

    # 归一化处理
    save_hero_info = save_hero_info.iloc[:,1:5]
    norm = (save_hero_info - save_hero_info.min()) / (save_hero_info.max() - save_hero_info.min())
    # print(norm)


'''执行'''
def main():
    save_hero_info()    # 王者荣耀英雄基本信息
    save_get_hero_clo() # 王者荣耀英雄皮肤
    save_skills_info()  # 王者荣耀英雄技能介绍
    save_mingwen_sugg() # 王者荣耀英雄铭文搭配推荐
    save_plus_sugg()    # 王者荣耀英雄技能加点建议
    save_equip_sugg()   # 王者荣耀英雄出装建议
    get_relates_list()  # 王者荣耀英雄关系
    # pretreatment()      # 预处理

url = 'https://pvp.qq.com/web201605/herolist.shtml'
main()

print("*****"*10)
print("运行结束！！！")