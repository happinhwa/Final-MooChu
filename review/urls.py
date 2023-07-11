from django.urls import path
from . import views

app_name = 'review'

urlpatterns = [
    # 리뷰
    path('main_review_list/<int:movie_id>/', views.main_review_list, name='main_review_list'),
    path('main_review_detail/<int:review_id>/', views.main_review_detail, name='main_review_detail'),
    path('write_review/<int:movie_id>/', views.write_review, name='write_review'),
    path('movies/', views.movie_list, name='movie_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('write_comment/<int:review_id>/', views.write_comment, name='write_comment'),
    # path('delete_comment/<int:review_id>/', views.delete_comment, name='delete_comment'),
]
