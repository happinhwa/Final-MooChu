from django.urls import path
from . import views

app_name = 'mlist'
urlpatterns = [
    path('movies/', views.movielist, name='movie_list'),
    path('movies/<str:ott>/', views.ott_movie_list, name='ott_movie_list'),
    path('movies/movie/<int:id>/', views.movie_detail_by_id, name='movie_detail_by_id'),
    path('detail/<int:id>/', views.movie_detail, name='movie_detail'),
    # 개봉예정작
    path('coming/', views.c_net, name='coming_soon'),
    
    # 상세정보
    path('detail/<int:id>/', views.moviedetail, name='moviedetail'),
    #path("mylist/add/", views.add_to_mylist, name="add_to_mylist"),
    #찜하기, 평점 설정
    path('add_to_mylist/<int:id>/', views.add_to_mylist, name='add_to_mylist'),
    path('detail/<int:id>/', views.movie_detail, name='movie_detail_with_list'),
    path('movie_rating/<int:id>/', views.movie_rating, name='movie_rating'),
    # 영화 리뷰 관련
    
    
    
   # path('review/<int:id>', views.media_review_by_id, name = 'review_by_id'),
   # path('postreview/<int:id>', views.post_review, name= 'post_reivew'),
   # path('vote/review/<int:review_id>', views.vote_reivew, name = 'vote_review'), # 리뷰 추천?
    
]