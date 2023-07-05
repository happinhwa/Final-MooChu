from django.urls import path
from . import views

app_name = 'mlist'

urlpatterns = [
    path('', views.movie_list, name='mlist'),
    path('c_net', views.c_net, name='mlist_net'), #넷플릭스 개봉예정
]
