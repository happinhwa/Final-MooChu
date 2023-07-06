from django.urls import path
from . import views

app_name = 'mlist'

urlpatterns = [
    path('page=<int:page_number>/', views.movie_list, name='mlist_page'),  # 페이지 번호를 동적 경로로 변경합니다.
    path('', views.movie_list, name='mlist'),  # 페이지 번호를 동적 경로로 변경합니다.
    path('comming', views.c_net, name='comming_soon'), # 개봉예정
]