from django.urls import path
from common.views import register, registration_complete
from . import views
app_name = 'common'

urlpatterns = [
    path('register/', register, name='register'),
    path('register_complete/', registration_complete, name='registration_complete'),
    path('login/',views.login ,name="login"), ## 로그인 url 
]
