from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'moochu'

urlpatterns =[
    path('', views.mainpage, name="main"),
    path('<str:media_type>/<str:ott>/', views.ott_media_list, name='ott_media_list'),
    path('<str:media_type>/<str:ott>/genre_filter/', views.genre_filter, name='genre_filter'),
]