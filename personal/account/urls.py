from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.custom_login, name='login'),
    path('signup/', views.custom_signup, name='signup'),
    path('logout/', views.custom_logout, name='logout'),
]