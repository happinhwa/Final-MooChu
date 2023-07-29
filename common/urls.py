from django.urls import path
from . import views


app_name = 'common'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_complete/', views.register_complete, name='register_complete'),
    path('activate/<str:uidb64>/<str:token>/', views.activate, name="activate"),
    path('authentication/', views.authentication, name="authentication"),
<<<<<<< HEAD
    path('genre_selection/', views.genre_selection, name='genre_selection'), 
=======
    path('genre_select/', views.genre_selection, name='genre_selection'), 
>>>>>>> 78dda2db6ec9df1197acf1229b90aa25c1e030a3
    path('save_genre/',views.save_genre, name='save_genre'),
    path('movie_selection/', views.movie_selection, name='movie_selection'),
]
