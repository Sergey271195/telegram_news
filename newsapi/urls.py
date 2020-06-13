from django.urls import path, include
from .views import NewsSender

NS = NewsSender()

urlpatterns = [
    path('', NS.dispatch)
]