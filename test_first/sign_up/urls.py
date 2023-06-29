from django.urls import path
from sign_up import views

# 모든 url 리스트

app_name = 'sign_up'

urlpatterns = [
    path('select_genre/', views.select_genre, name='select_genre'),
    path('select_content/', views.select_content, name='select_content'),
]