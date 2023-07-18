from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'moochu'

urlpatterns =[
<<<<<<< HEAD
    path('main', views.main, name="main"),
=======
    path('', views.mainpage, name="main"),
>>>>>>> b654d956433a7c43374b3131e7f081a3d78e63b6
]