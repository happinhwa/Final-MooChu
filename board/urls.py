from django.urls import path
from . import views

app_name = 'board'

urlpatterns = [
    path('moobo', views.moobo, name='moobo'), # post list 페이지
    path('post', views.post, name='post'), # post upload 페이지
    path('post_detail/<int:post_id>', views.detail, name='post_detail'), 
    path('comment/create/post/<int:post_id>/', views.comment_create, name='comment_create'), # comment upload 페이지
    path('vote/post/<int:post_id>/', views.vote_post, name='vote_post'), # 글 정말 추천하시겠읍니까? 페이지
    path('vote/comment/<int:comment_id>/', views.vote_comment, name='vote_comment'), # 댓글 정말 추천하시겠읍니까? 페이지
]
