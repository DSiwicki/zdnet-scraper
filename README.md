# zdnet-scraper

Scraper was created on 2018 for the purposes of my text mining project that contained analysis of articles on security topic. Codes were refreshed on December 2020.

The project include 4 functions:

```python 

def full_driver()

```


```python 

def get_topics(driver: webdriver.chrome.webdriver.WebDriver)

```

```python

def get_articles_links(topic_url: str, 
                       delta, 
                       driver: webdriver.chrome.webdriver.WebDriver
                      )
```

```python

def get_articles(articles_links: list, 
                 driver: webdriver.chrome.webdriver.WebDriver
                )
```




