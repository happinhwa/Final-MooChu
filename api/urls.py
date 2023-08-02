from django.urls import path
from . import views

urlpatterns = [
    path('movies/', views.movielist, name='movie_list'),
    path('movies/<str:ott>/', views.ott_movie_list, name='ott_movie_list'),
    path('genre_filter/', views.genre_filter, name='genre_filter')
    # path('genre/', genre_filter, name='genre_filter'),
]
