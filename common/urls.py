from django.urls import path
from common.views import register, registration_complete,firstmovie,genre_selection

app_name = 'common'

urlpatterns = [
    path('register/', register, name='register'),
    path('register_complete/', registration_complete, name='registration_complete'),
    path('firstmovie/', firstmovie, name='firstmovie'),
    path('genre_selection/', genre_selection, name='genre_selection'),

]
