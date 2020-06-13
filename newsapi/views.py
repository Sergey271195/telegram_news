from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
import os
from .customTg import TelegramBot, createLineKeyboard, createRowKeyboard, bot_command_decorator
from .newsgetter import NewYorkTimesNews, BBCNews, RollingStoneNews, FoxNews, KPNews, RIANews, RBKNews

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
        self.NYTNews = []

        self.BBC = BBCNews()
        self.BBCNews = []

        self.RST = RollingStoneNews()
        self.RSTNews = []
        
        self.FOX = FoxNews()
        self.FOXNews = []

        self.KP = KPNews()
        self.KPNews = []

        self.RIA = RIANews()
        self.RIANews = []

        self.RBK = RBKNews()
        self.RBKNews = []

        self.news_sources = {
            'NYT': {
                'class': self.NYT,
                'list': self.NYTNews
            },
            'BBC': {
                'class': self.BBC,
                'list': self.BBCNews
            },
            'RST': {
                'class': self.RST,
                'list': self.RSTNews
            },
            'FOX': {
                'class': self.FOX,
                'list': self.FOXNews
            },
            'KP': {
                'class': self.KP,
                'list': self.KPNews
            },
            'RIA': {
                'class': self.RIA,
                'list': self.RIANews
            },
            'RBK': {
                'class': self.RBK,
                'list': self.RBKNews
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


    def send_news(self, news_src, user_id, message_id = None, data = None):

        news_source = self.news_sources[news_src].get('class')
        news_array = self.news_sources[news_src].get('list')

        if not data:
            news_array.clear()
            news_source.get_articles()
            news_array += news_source.prepare_messages()
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
            reply = self.tgBot.sendMessage(user_id, text = 'Article\n' + news_array[current_article], parse_mode='HTML', reply_markup=createLineKeyboard(LAYOUT))
        else:
            reply = self.tgBot.editMessageText(user_id, message_id, 'Article\n' + news_array[current_article], parse_mode='HTML', reply_markup=createLineKeyboard(LAYOUT))



    def callback_handler(self, callback_query):
        user_id = callback_query['from'].get('id')
        message_id = callback_query['message'].get('message_id')
        data = callback_query.get('data')
        if data in NEWS_SOURCES_NAMES:
            print(data)
            self.send_news(news_src = data, user_id = user_id)
        elif any(list(map(lambda x: x in data, NEWS_SOURCES_NAMES))):
            news_src, next_article = data.split('_')
            self.send_news(news_src, user_id, message_id, int(next_article))

    def post(self, request):
        request_body = json.loads(request.body)
        callback_query = request_body.get('callback_query')
        message = request_body.get('message')
        print(request_body)
        self.return_news_sources_keyboard(request_body, user_id = None)
        if callback_query:
            self.callback_handler(callback_query)
        return(HttpResponse(200))

        