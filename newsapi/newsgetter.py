import requests
from bs4 import BeautifulSoup
import re


class BBCNews():

    def __init__(self):
        self.url = "https://www.bbc.com/news"
        self.href = re.compile(r'href="(?P<href>.*?)"')
        self.text = ''
        self.articles = []

    def get_articles(self):
        self.articles = []
        all_articles = requests.get(self.url)
        if all_articles.status_code == 200:
            self.text = all_articles.text
            soup = BeautifulSoup(self.text, 'html.parser')
            articles = soup.find_all('a', class_ = "gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor")
            for article in articles:
                href = re.search(self.href, str(article))
                if href:
                    article_href = href.group('href')
                    if 'https' in article_href:
                        self.articles.append(article_href)
                    else:
                        self.articles.append('https://www.bbc.com'+article_href)

    def prepare_messages(self):
        messages = []
        for href in self.articles:
            message = f'<a href="{href}">Full Article</a>'
            messages.append(message)
        return messages

class NewYorkTimesNews():

    def __init__(self):
        self.url = "https://www.nytimes.com/"
        self.headline_expr = re.compile(r'<h2 class="(css-1vvhd4r|css-z9cw67|css-1cmu9py|css-1yxu27x) e1voiwgp0">(<span>)?(?P<headline>.*?)(</span>)?</h2>')
        self.img_expr = re.compile(r'<img .*?src="(?P<image>.*?)"/>')
        self.paragraph_expr = re.compile(r'<p class="css-1pfq5u e1lfvv700">(?P<paragraph>.*?)</p>')
        self.ul_expr = re.compile(r'<ul class="css-ip5ca7 e1lfvv701">(?P<ul>.*?)</ul>')
        self.li_expr = re.compile(r'<li>(?P<li>.*?)</li>')
        self.href_expr = re.compile(r'<a(.*?)href="(?P<href>.*?)">')
        self.text = ''
        

    def get_articles(self):
        nyt = requests.get(self.url)
        if nyt.status_code == 200:
            self.text = nyt.text

    
    def prepare_messages(self):
        messages = []
        if self.text:
            soup = BeautifulSoup(self.text, 'html.parser')
            articles = soup.find_all('article', class_ = "css-8atqhb")
            for index, article in enumerate(articles):
                headline = re.search(self.headline_expr, str(article))
                article_href = re.search(self.href_expr, str(article))
                message = ''
                if headline:
                    if article_href:
                        href = article_href.group('href')
                        message = f'<a href="https://www.nytimes.com{href}">Full Article</a>'

                    messages.append(message)
            return(messages)


class RollingStoneNews():

    def __init__(self):
        self.url = "https://www.rollingstone.com/"
        self.href = re.compile(r'href="(?P<href>.*?)"')
        self.text = ''
        self.articles = []

    def get_articles(self):
        self.articles = []
        all_articles = requests.get(self.url)
        if all_articles.status_code == 200:
            self.text = all_articles.text
            soup = BeautifulSoup(self.text, 'html.parser')
            articles = soup.find_all('a', class_ = "c-card__wrap")
            for article in articles:
                href = re.search(self.href, str(article))
                if href:
                    article_href = href.group('href')
                    self.articles.append(article_href)

    def prepare_messages(self):
        messages = []
        for href in self.articles:
            message = f'<a href="{href}">Full Article</a>'
            messages.append(message)
        return messages

class FoxNews():

    def __init__(self):
        self.url = "https://www.foxnews.com/"
        self.href = re.compile(r'href="(?P<href>.*?)"')
        self.text = ''
        self.articles = []

    def get_articles(self):
        self.articles = []
        all_articles = requests.get(self.url)
        if all_articles.status_code == 200:
            self.text = all_articles.text
            soup = BeautifulSoup(self.text, 'html.parser')
            articles = soup.find('main', class_ = "main-content")
            href = re.findall(self.href, str(articles))
            for ref in href:
                if ('https' in ref) and (ref not in self.articles):
                    self.articles.append(ref)


    def prepare_messages(self):
        messages = []
        for href in self.articles:
            message = f'<a href="{href}">Full Article</a>'
            messages.append(message)
        return messages

class KPNews():

    def __init__(self):
        self.url = "https://www.kp.ru/"
        self.href = re.compile(r'href="(?P<href>.*?)"')
        self.url_expr = re.compile(r'"url":"(?P<href>/daily/\d+.*?)"')
        self.text = ''
        self.articles = []

    def get_articles(self):
        self.articles = []
        all_articles = requests.get(self.url)
        if all_articles.status_code == 200:
            self.text = all_articles.text
            soup = BeautifulSoup(self.text, 'html.parser')
            href = re.findall(self.url_expr, str(soup))
            for ref in href:
                if ('https' not in ref) and ('daily' in ref) and (ref not in self.articles):
                    self.articles.append('https://www.kp.ru'+ref)


    def prepare_messages(self):
        messages = []
        for href in self.articles:
            message = f'<a href="{href}">Full Article</a>'
            messages.append(message)
        return messages


class RIANews():

    def __init__(self):
        self.url = "https://ria.ru/"
        self.href = re.compile(r'href="(?P<href>.*?)"')
        self.text = ''
        self.articles = []

    def get_articles(self):
        self.articles = []
        all_articles = requests.get(self.url)
        if all_articles.status_code == 200:
            self.text = all_articles.text
            soup = BeautifulSoup(self.text, 'html.parser')
            articles = soup.find_all('a', class_ = "cell-list__item-link color-font-hover-only")
            for article in articles:
                href = re.search(self.href, str(article))
                if href:
                    article_href = href.group('href')
                    if article_href not in self.articles:
                        self.articles.append(article_href)


    def prepare_messages(self):
        messages = []
        for href in self.articles:
            message = f'<a href="{href}">Full Article</a>'
            messages.append(message)
        return messages

class RBKNews():

    def __init__(self):
        self.url = "https://www.rbc.ru/"
        self.href = re.compile(r'href="(?P<href>.*?)"')
        self.text = ''
        self.articles = []

    def get_articles(self):
        self.articles = []
        all_articles = requests.get(self.url)
        if all_articles.status_code == 200:
            self.text = all_articles.text
            soup = BeautifulSoup(self.text, 'html.parser')
            articles = soup.find_all('a', class_ = "main__feed__link js-yandex-counter")
            for article in articles:
                href = re.search(self.href, str(article))
                if href:
                    article_href = href.group('href')
                    if article_href not in self.articles:
                        self.articles.append(article_href)


    def prepare_messages(self):
        messages = []
        for href in self.articles:
            message = f'<a href="{href}">Full Article</a>'
            messages.append(message)
        return messages

if __name__ == "__main__":
    RBK = RBKNews()
    RBK.get_articles()
    RBK.prepare_messages()
    #print(message_list)



