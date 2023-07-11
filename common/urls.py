from django.urls import path
from common.views import register, register_complete
from . import views

app_name = 'common'

urlpatterns = [
    path('register/', register, name='register'),
    path('register_complete/', register_complete, name='register_complete'),
    path('login/',views.login ,name="login"), ## 로그인 url 
]
