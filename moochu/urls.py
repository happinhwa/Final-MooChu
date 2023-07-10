from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'moochu'

urlpatterns =[
    path('mainpage', views.mainpage, name="mainpage"),
]