# zdnet-scraper

Scraper was created on 2018 for the purposes of my text mining project that contained analysis of articles on security topic. Codes were refreshed in December 2020.

The project include 4 functions:

```python 

def full_driver()

```

That establish connection with Chrome and set chrome_options.


```python 

def get_topics(driver: webdriver.chrome.webdriver.WebDriver
              )

```

That allows to list available topics (function is not neccessary to run).



```python

def get_articles_links(topic_url: str, 
                       delta, 
                       driver: webdriver.chrome.webdriver.WebDriver
                      )
```

That allows to get links (and some basic information) to articles in provided time period.


```python

def get_articles(articles_links: list, 
                 driver: webdriver.chrome.webdriver.WebDriver
                )
```

That allows to get articles' texts.


In order to scrap articles you have to provide chosen time delta and topic for **get_articles_links()** function




