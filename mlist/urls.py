from django.urls import path
from . import views

app_name = 'mlist'
urlpatterns = [
    path('movies/', views.movielist, name='movie_list'),
    path('movies/<str:ott>/', views.ott_movie_list, name='ott_movie_list'),
    path('movies/movie/<int:id>/', views.movie_detail_by_id, name='movie_detail_by_id'),  # Add this line
    path('comming/', views.c_net, name='comming_soon'),
    path('detail/<int:id>/', views.moviedetail, name='moviedetail'),
]


#from django.urls import path, include
#from . import views
#
#app_name = 'mlist'
#urlpatterns = [
#    path('movies/', views.movielist, name='movie_list'),
#    path('movies/<str:ott>/', views.ott_movie_list, name='ott_movie_list'),
#    # path('genre/', genre_filter, name='genre_filter'),
#]

#
#urlpatterns = [
#    path('', views.redirect_to_movie_list, name='redirect_to_movie_list'),  # 새로운 URL 패턴 추가
#    path('page=<int:page_number>/', views.movie_list, name='mlist_page'),
#    path('comming', views.c_net, name='comming_soon'),
##    path('<int:movie_id>/', views.movie_detail, name='detail'),
#]