from django.urls import path
from . import views
app_name = 'common'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_complete/', views.registration_complete, name='registration_complete'),
    path('mypage/', views.mypage_home, name="mypage"),
    path('mypage/mylist/', views.mypage_mylist, name="mylist"),
    path('mypage/reviews/', views.mypage_reviews, name="reviews"),
    path('mypage/note/', views.mypage_note, name="note"),
    path('genre_select/', views.genre_selection, name='genre_selection'), 
    ## 로그인이랑 회원가입 완료되면
    # path('mypage/<user.id>/', views.mypage_home, name="mypage"),
    # path('mypage/<user.id>/mylist', views.mypage_mylist, name="mylist"),
    # path('mypage/<user.id>/reviews', views.mypage_reviews, name="reviews"),
    # path('mypage/<user.id>/note', views.mypage_note, name="note"),
    # path('mypage/<user.id>/edit', views.mypage_edit, name="edit"),

    ## 방명록 삭제
    path('delete/<int:guestnote_id>/', views.delete, name="delete"),
    
]
