from selenium import webdriver
from bs4 import BeautifulSoup

from datetime import datetime
from time import sleep



def full_driver():
    
    driver_path = './src/chromedriver'
    
    chrome_options = webdriver.ChromeOptions()
    
    chrome_options.add_argument('--window-size=1360,700')
    driver = webdriver.Chrome(driver_path, options = chrome_options)
    driver.set_page_load_timeout(180)
    
    return driver



def get_topics(driver: webdriver.chrome.webdriver.WebDriver 
              ):
    
    driver.get('https://www.zdnet.com/topic')
    
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")

    navs = soup.find(class_ = 'nav nav-tabs topic-nav')
    nav_list = [nav.find('a')['href'] for nav in navs.findChildren("li" , recursive=False) if 'alpha' in nav.find('a')['href']]
    
    topics_all = {}
    print(nav_list)
    
    for nav in nav_list:
        
        nav_url = 'https://www.zdnet.com' + nav
          
        driver.get(nav_url)
        print(driver.current_url)
       
        while True:
                 
            topics  = {}
            
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            topics_ul = soup.find_all(class_ = 'col-2')
            topics = {(topic.find('a').getText()) : (topic.find('a')['href']) for topic in topics_ul 
              if 'topic' in topic.find('a')['href'] and topic.find('a')['href'] != 'https://www.zdnet.com/topic/'}

            topics_all = {**topics_all, **topics}

            try:
                next_button = driver.find_element_by_css_selector('a.next')
                next_button.click()
                
            except:
                break
                
        sleep(5)
        
    return topics_all



def get_articles_links(topic_url: str, 
                       delta, 
                       driver: webdriver.chrome.webdriver.WebDriver
                      ):
    
    articles_all = []
    
    i = 1
    
    time_border = datetime.now() - delta
    print("Scraping articles since: " + str(time_border)[:19])
    
    while True:
        
        try:
            url = 'https://www.zdnet.com' + topic_url + str(i)
            driver.get(url)
            
            i += 1
            
            sleep(5)
        
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
        
            latest_articles = soup.find(id = 'topic-river-latest')
            content = latest_articles.findAll(class_ = "content")
            
            article_data = [[item.find('h3').find('a').getText(), 
                                item.find('h3').find('a')['href'],
                                item.findAll('p')[1].find('a').getText(),
                                item.findAll('p')[1].find('span')['data-date'],
                                item.find('p').getText()
                               ] for item in content if 'promo' not in item.parent.parent['class']]
              
            articles_all = articles_all + article_data       
            
            print(driver.current_url)
            
            if datetime.strptime(article_data[-1][3], '%Y-%m-%d %H:%M:%S') < time_border:
                print('Time border exceeded')
                break
        except:
            break

    print(len(articles_all))
    
    return articles_all



def get_articles(articles_links: list, 
                 driver: webdriver.chrome.webdriver.WebDriver
                ):
    
    articles_data = []
    
    for link in articles_links:
        
        url = 'https://www.zdnet.com' + link
        driver.get(url)
        
        sleep(3)
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        
        header = soup.find(class_ = 'storyHeader article')
        title = header.find('h1').getText()
        summary = header.find('p').getText()
        
        body = soup.find('article')
        
        meta = body.find(class_ = 'meta')
        
        author = meta.find(rel = "author").findChild('span').getText()
        publication_date = meta.find('time').get('datetime')
        topic = meta.find('a', attrs = {'rel': None}).getText()

        text = body.find(class_ = 'storyBody').findAll('p')
        text_list = [item.getText() for item in text 
              if ("See also:" not in item.getText()) and (item.parent.has_attr('class'))
             ]
        article_text = '\n\n'.join(text_list)
        
        articles_data.append([url, title, summary, author, publication_date, topic, article_text])
        
        print(url)
             
    return articles_data
    