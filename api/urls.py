from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movielist, name='movie_list'),
    path('movies/<str:ott>/', views.ott_movie_list, name='ott_movie_list')
]
