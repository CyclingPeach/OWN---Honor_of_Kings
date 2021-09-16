def get_all_hero_urls(url):
    
    response = requests.get(url ,)
    response.encoding = response.apparent_encoding    # 获取网页真实编码'GB2312'
    html = response.text
    soup = BeautifulSoup(html)
    
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
       
    return list(zip(hero_name_lists, hero_url_lists))