from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'review'

urlpatterns =[
    path('<str:movie_id>/detail/media/rating', views.media_rating, name='media_rating'),
    path('', views.review, name="review"),
    path('<str:movie_id>/upload/', views.review_upload, name='review_upload'),
    path('<str:movie_id>/detail/<int:review_id>/', views.review_detail, name='review_detail'),

    
]