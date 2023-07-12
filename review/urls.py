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
    path('review_update/<int:review_id>/', views.review_update, name='review_update'),
    path('comment_update/<int:comment_id>/', views.comment_update, name='comment_update'),
    path('review_delete/<int:review_id>/', views.review_delete, name='review_delete'),
    path('comment_delete/<int:comment_id>/', views.comment_delete, name='comment_delete'),
    path('review_liker1/<int:review_id>/', views.review_liker1, name='review_liker1'),
    path('review_liker2/<int:review_id>/', views.review_liker2, name='review_liker2'),
]
