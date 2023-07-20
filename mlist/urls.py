from django.urls import path
from . import views

app_name = 'mlist'
urlpatterns = [
    path('movies/', views.movielist, name='movie_list'),
    path('movies/<str:ott>/', views.ott_movie_list, name='ott_movie_list'),
    path('movies/movie/<int:id>/', views.movie_detail_by_id, name='movie_detail_by_id'),
    path('movie_detail/<int:id>/', views.movie_detail, name='movie_detail'),
    path('coming/', views.c_net, name='coming_soon'),
    path('detail/<int:id>/', views.moviedetail, name='moviedetail'),
    path('write_review/<int:id>/', views.write_review, name='write_review'),
]