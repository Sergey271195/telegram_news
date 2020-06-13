from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from customTg import TelegramBot, createLineKeyboard
from .newsgetter import NewYorkTimesNews

LAYOUT = [
    ('Prevous', 'new'),
    ('Cuurent number', 'Length'),
    ('Next', 'new1'),
]


class NewsSender():

    def __init__(self):
        self.NYT = NewYorkTimesNews()
        self.tgBot = TelegramBot()
        self.nyt_message_list = []

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

    def post(self, request):
        request_body = json.loads(request.body)
        callback_query = request_body.get('callback_query')
        message = request_body.get('message')
        print(request_body)
        if callback_query:
            print('CALLBACK')
            user_id = callback_query['from'].get('id')
            message_id = callback_query['message'].get('message_id')
            data = callback_query.get('data')
            try:
                next_article = int(data) % len(self.nyt_message_list)
                print(next_article)
                LAYOUT = [
                    (next_article-1, 'Previous'),
                    ('hi', f'{next_article+1}/{len(self.nyt_message_list)}'),
                    (next_article+1, 'Next')
                ]
                reply = self.tgBot.editMessageText(user_id, message_id, text = 'Article\n' + self.nyt_message_list[next_article], parse_mode='HTML', reply_markup=createLineKeyboard(LAYOUT))
                print(reply)
            except Exception as e:
                print(e)
            
            
        elif message:
            user_id = message['from'].get('id')
            self.NYT.get_articles()
            self.nyt_message_list = self.NYT.prepare_messages()
            print('MESSAGES RECIEVED')
            print(self.nyt_message_list)
            number_of_articles = len(self.nyt_message_list)
            LAYOUT = [
                (number_of_articles-1, 'Previous'),
                ('hi', f'1/{number_of_articles}'),
                (1, 'Next')
            ]

            self.tgBot.sendMessage(user_id, 'Article\n' + self.nyt_message_list[0], parse_mode='HTML', reply_markup=createLineKeyboard(LAYOUT))
        return(HttpResponse("200"))

        