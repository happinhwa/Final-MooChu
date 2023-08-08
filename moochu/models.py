from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

from django.db import models
from django.utils import timezone
from django.conf import settings
from pymongo import MongoClient

# db 연결
mongo_client = MongoClient(settings.MONGODB_URL)

media_db= mongo_client[settings.ALL_MONGODB_NAME]

daum_db = mongo_client[settings.DAUM_MONGODB_NAME]

class Media:
    collection=media_db.movies2




# 개봉예정작 관련입니다.
class DaumMovie:
    collection = None

    def __init__(self, img_link):
        self.img_link = img_link

    def save(self):
        self.collection.insert_one({
            'img_link': self.img_link.lower()
        })

    @classmethod
    def get_all_movies(cls):
        movies = cls.collection.find({}, {'title': 1, 'img_link': 1})
        titles = [movie['img_link'] for movie in movies]
        return titles


class DNetflixMovie(DaumMovie):
    collection = daum_db['daumnetflix']

    @classmethod
    def get_all_movies(cls):
        movies = cls.collection.find({}, {'num': 1, 'title': 1, 'img_link': 1})
        return list(movies)


class DWatchaMovie(DaumMovie):
    collection = daum_db['daumwatcha']

    @classmethod
    def get_all_movies(cls):
        movies = cls.collection.find({}, {'num': 1, 'title': 1, 'img_link': 1})
        return list(movies)

class CMovie(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.source = None
        self.num = None
        self.logo_image = None  # Add the 'logo_image' attribute to store the logo image path
