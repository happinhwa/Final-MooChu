from django.urls import path
from . import views


app_name = 'common'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_complete/', views.register_complete, name='register_complete'),
<<<<<<< HEAD
    path('genre_select', views.genre_selection, name='genre_selection'), 
    ## 로그인이랑 회원가입 완료되면
    # path('mypage/<user.id>/', views.mypage_home, name="mypage"),
    # path('mypage/<user.id>/mylist', views.mypage_mylist, name="mylist"),
    # path('mypage/<user.id>/reviews', views.mypage_reviews, name="reviews"),
    # path('mypage/<user.id>/note', views.mypage_note, name="note"),
    # path('mypage/<user.id>/edit', views.mypage_edit, name="edit")
=======
    path('activate/<str:uidb64>/<str:token>/', views.activate, name="activate"),
    path('authentication/', views.authentication, name="authentication")
    path('genre_selection/', views.genre_selection, name='genre_selection'), 
    path('save_genre/',views.save_genre, name='save_genre'),
    path('movie_selection/', views.movie_selection, name='movie_selection'),
>>>>>>> b654d956433a7c43374b3131e7f081a3d78e63b6
]
