from django.urls import path
from common.views import login, register, registration_complete, genre_selection

app_name = 'common'

urlpatterns = [
    path('login', login, name='login'),
    path('register/', register, name='register'),
    path('register_complete/', registration_complete, name='registration_complete'),
    path('genre_select', genre_selection, name='genre_selection'), 
]
