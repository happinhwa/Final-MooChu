from django.urls import path
from . import views

app_name = 'mlist'

urlpatterns = [
    path('', views.redirect_to_movie_list, name='redirect_to_movie_list'),  # 새로운 URL 패턴 추가
    path('page=<int:page_number>/', views.movie_list, name='mlist_page'),
    path('comming', views.c_net, name='comming_soon'),
    path('<int:movie_id>/', views.movie_detail, name='detail'),
]