from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_complete/', views.register_complete, name='register_complete'),


    
]
