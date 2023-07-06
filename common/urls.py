from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_complete/', views.register_complete, name='register_complete'),
    path('genre_selection/', views.genre_selection, name='genre_selection'), 
    path('save_genre/',views.save_genre, name='save_genre'),
    path('movie_selection/', views.movie_selection, name='movie_selection'),

    ## 로그인이랑 회원가입 완료되면
    path('mypage/<str:nickname>/', views.mypage_home, name="mypage"),
    path('mypage/<str:nickname>/mylist', views.mypage_mylist, name="mylist"),
    path('mypage/<str:nickname>/reviews', views.mypage_reviews, name="reviews"),
    path('mypage/<str:nickname>/note', views.mypage_note, name="note"),
    path('mypage/<str:nickname>/edit', views.mypage_edit, name="edit"),

    ## 방명록 삭제
    path('delete/<int:guestnote_id>/', views.delete, name="delete"),

    ## 사용자의 리뷰 전체 list
    path('reviews/', views.reviews_total, name="reviews_total"),

    ## 사용자의 평점 전체 list
    path('votes/', views.votes, name="votes"),

    ## 팔로우 
    path('follow/create', views.follow, name="follow"),
    ## 팔로우 취소 
    path('follow/delete', views.follow_de, name="follow_de"),
]
