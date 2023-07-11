from django.urls import path
<<<<<<< HEAD
from . import views

app_name = 'common'

urlpatterns = [
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_complete/', views.register_complete, name='register_complete'),


    
=======
from common.views import register, registration_complete
from . import views
app_name = 'common'

urlpatterns = [
    path('register/', register, name='register'),
    path('register_complete/', registration_complete, name='registration_complete'),
    path('login/',views.login ,name="login"), ## 로그인 url 
>>>>>>> 3032e914fe1914a652206ebf0f7c3eb61199ceca
]
