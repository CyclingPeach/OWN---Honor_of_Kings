def print_one_hero_soup(one_hero_url):
    one_hero_response = requests.get(one_hero_url)
    one_hero_response.encoding = one_hero_response.apparent_encoding    # 获取网页真实编码    https://www.cnblogs.com/bw13/p/6549248.html
    one_hero_html = one_hero_response.text
    one_hero_soup = BeautifulSoup(one_hero_html, 'html.parser')    # BeautifulSoup 解析网页，获取源代码
    
    return one_hero_soup


def print_one_hero_xpath(one_hero_url):
    
    options = webdriver.ChromeOptions()
    options.headless = True    # 不弹出 Chrome浏览器界面，后台运行
    driver = webdriver.Chrome(chrome_options = options)    # 控制chrome浏览器
    
    driver.get(one_hero_url)
    time.sleep(2)
    content = driver.page_source    # selenium 获取网页源代码
    cont_xph = lxml.etree.HTML(content)    # 解析 content 
    
    return cont_xph