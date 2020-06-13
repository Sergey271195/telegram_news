import requests
from bs4 import BeautifulSoup
import json
import re, os
from customTg import createLineKeyboard

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
        self.message_list = []
        if self.text:
            soup = BeautifulSoup(self.text, 'html.parser')
            articles = soup.find_all('article', class_ = "css-8atqhb")
            for index, article in enumerate(articles):
                headline = re.search(self.headline_expr, str(article))
                message = ''
                if headline:
                    #message+= '<b>'+ headline.group('headline')+'</b>\n'
                    image = re.search(self.img_expr, str(article))
                    paragraph = re.search(self.paragraph_expr, str(article))
                    ul = re.search(self.ul_expr, str(article))
                    article_href = re.search(self.href_expr, str(article))
                    if image:
                        src = image.group('image')
                        #message+= f'<a href="{src}">&#8204;</a>'
                    if paragraph:
                        pass
                        #message+= '\t\t\t\t' + paragraph.group('paragraph')+'\n'
                    if ul:
                        lis = re.findall(self.li_expr, ul.group('ul'))
                        for li in lis:
                            pass
                            #message+= '\t\t\t\t - '+li +'\n'
                    if article_href:
                        href = article_href.group('href')
                        message+= f'<a href="https://www.nytimes.com{href}">&#8204;</a>'

                    self.message_list.append(message)
            print(self.message_list)
            return(self.message_list)

if __name__ == "__main__":
    message_list = NewYorkTimesNews().prepare_messages()
    print(message_list)



