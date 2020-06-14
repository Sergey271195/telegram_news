from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import os
from datetime import datetime, timedelta
from django.utils.timezone import now

from .customTg import TelegramBot, createLineKeyboard, createRowKeyboard, bot_command_decorator
from .newsgetter import NewYorkTimesNews, BBCNews, RollingStoneNews, FoxNews, KPNews, RIANews, RBKNews
from .models import NewsSource, Article

NEWS_SOURCES = [
    ('NYT','New York Times'),
    ('BBC','BBC'),
    ('RST','Rolling Stone'),
    ('FOX','FOX News'),
    ('KP','KP News'),
    ('RIA','RIA News'),
    ('RBK','RBK News'),
]

NEWS_SOURCES_NAMES = [
    'NYT', 'BBC', 'RST', 'FOX', 'KP', 'RIA', 'RBK'
]



class NewsSender():

    def __init__(self):
        self.tgBot = TelegramBot()

        self.NYT = NewYorkTimesNews()
        self.BBC = BBCNews()
        self.RST = RollingStoneNews()  
        self.FOX = FoxNews()
        self.KP = KPNews()
        self.RIA = RIANews()
        self.RBK = RBKNews()

        self.news_sources = {
            'NYT': {
                'class': self.NYT,
                'fullname': 'New York Times',
            },
            'BBC': {
                'class': self.BBC,
                'fullname': 'BBC',
            },
            'RST': {
                'class': self.RST,
                'fullname': 'Rolling Stone',
            },
            'FOX': {
                'class': self.FOX,
                'fullname': 'FOX News',
            },
            'KP': {
                'class': self.KP,
                'fullname': 'KP News',
            },
            'RIA': {
                'class': self.RIA,
                'fullname': 'RIA News',
            },
            'RBK': {
                'class': self.RBK,
                'fullname': 'RBK News',
            }
        }

    @csrf_exempt
    def dispatch(self, request):
        if request.method == 'GET':
            response = self.get(request)
            return response

        elif request.method == 'POST':
            response = self.post(request)
            return response


    def get(self, request):
        if request.method == "GET":
            return(HttpResponse("<h1>News Bot Api</h1>"))

    @bot_command_decorator('/news')
    def return_news_sources_keyboard(self, request_body, user_id):
        self.tgBot.sendMessage(user_id, text = 'News Sources', reply_markup=createRowKeyboard(NEWS_SOURCES))


    def add_articles_to_db(self, news_source):
        short_name = news_source.short_name
        news_src = self.news_sources[short_name].get('class')
        news_src.get_articles()
        news_array = news_src.prepare_messages()
        for link in news_array:
            article = Article(news_source = news_source, link = link)
            article.save()

    def check_if_outdated(self, news_source):
        last_updated = news_source.last_updated
        short_name = news_source.short_name
        if (now()-last_updated) > timedelta(minutes = 30):
            Article.objects.all().filter(news_source = news_source).delete()
        self.add_articles_to_db(news_source)


    def send_news(self, news_src, user_id, message_id = None, data = None):

        news_array = Article.objects.all().filter(news_source__short_name = news_src)
        links_list = [article.link for article in news_array]

        if not data:
            current_article = 0
        else:
            current_article = data % len(news_array)
        news_array_length = len(news_array)
        LAYOUT = [
            (news_src+'_'+str(current_article-1), 'Previous'),
            ('Info', f'{current_article + 1}/{news_array_length}'),
            (news_src+'_'+str(current_article+1), 'Next')
        ]


        if not data:
            reply = self.tgBot.sendMessage(user_id, text = links_list[current_article], parse_mode='HTML', reply_markup=createLineKeyboard(LAYOUT))
        else:
            reply = self.tgBot.editMessageText(user_id, message_id, links_list[current_article], parse_mode='HTML', reply_markup=createLineKeyboard(LAYOUT))



    def callback_handler(self, callback_query):
        user_id = callback_query['from'].get('id')
        message_id = callback_query['message'].get('message_id')
        data = callback_query.get('data')
        if data in NEWS_SOURCES_NAMES:
            db_news_source_exists = NewsSource.objects.all().filter(short_name = data).exists()
            if db_news_source_exists:
                news_source = NewsSource.objects.all().get(short_name = data)
                self.check_if_outdated(news_source)
                
            else:
                news_source = NewsSource(name = self.news_sources[data].get('fullname'), short_name = data, last_updated = datetime.now())
                news_source.save()
                self.add_articles_to_db(news_source)
                
            self.send_news(news_src = data, user_id = user_id)
        elif any(list(map(lambda x: x in data, NEWS_SOURCES_NAMES))):
            news_src, next_article = data.split('_')
            self.send_news(news_src, user_id, message_id, int(next_article))

    def post(self, request):
        request_body = json.loads(request.body)
        callback_query = request_body.get('callback_query')
        message = request_body.get('message')
        self.return_news_sources_keyboard(request_body, user_id = None)
        if callback_query:
            self.callback_handler(callback_query)
        return(HttpResponse(200))

        