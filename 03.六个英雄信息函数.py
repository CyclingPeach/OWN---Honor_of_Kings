'''
    王者荣耀英雄基本信息
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
    if os.path.isfile('./王者荣耀英雄皮肤.csv') == True:
        os.remove('./王者荣耀英雄皮肤.csv')

    for one_hero_url in get_all_hero_urls(url):
        one_hero_soup = print_one_hero_soup(one_hero_url[1])
        try:
            get_hero_info(one_hero_soup)
        except:
            pass
        continue


'''
    王者荣耀英雄皮肤
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
            get_hero_clo(hero_name, one_hero_soup)
        except:
            pass
        continue


'''
    王者荣耀英雄技能介绍
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
    王者荣耀英雄铭文搭配推荐
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
    王者荣耀英雄技能加点建议
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
            print(one_hero_url)  # 实际运行后发现有三个英雄出现错误
            pass
        continue