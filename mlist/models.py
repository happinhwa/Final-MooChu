from django.db import models
from django.utils import timezone
from django.conf import settings
from pymongo import MongoClient

from common.models import User, MovieRating

# db 연결
mongo_client = MongoClient(settings.MONGODB_URI)

tmdb_db = mongo_client[settings.TMDB_MONGODB_NAME]
actor_db = mongo_client[settings.TMDB_MONGODB_ACTOR]
 
ott_db = mongo_client[settings.OTT_MONGODB_NAME]
ott_all_db = mongo_client[settings.OTT_ALLDB_NAME]

daum_db = mongo_client[settings.DAUM_MONGODB_NAME]



class Movie:
    collection = tmdb_db.movie

    @classmethod
    def get_collection(cls):
        return tmdb_db

    @classmethod
    def get_movie_by_id(cls, movie_id):
        collection = cls.get_collection().movie
        movie = collection.find_one({'id': movie_id})
        if movie:
            genre_names = [genre['name'] for genre in movie['genres']]
            movie['genres'] = genre_names
            return Movie(**movie)
        return None

    def __init__(self, id, title, release_date, runtime, poster_path, genres, overview):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.runtime = runtime
        self.poster_path = poster_path
        self.genres = genres
        self.overview = overview

    def save(self):
        collection = self.get_collection().movie
        collection.insert_one({
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'runtime': self.runtime,
            'poster_path': self.poster_path,
            'genres': self.genres,
            'overview': self.overview,
        })
    def save_review(self, user, review_text):
        # 해당 영화에 새 리뷰를 저장합니다.
        review = Review.objects.create(user=user, review=review_text, movie=self)
        return review

    def get_reviews(self):
        # 해당 영화에 대한 모든 리뷰를 가져옵니다.
        reviews = Review.objects.filter(movie=self)
        return reviews




# OTT별 데이터를 위한 base
class OTTMovie:
    collection = None

    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType):
        self.id = id
        self.titleKr = titleKr
        self.releasedAt = releasedAt
        self.posterImageUrl = posterImageUrl
        self.mediaType = mediaType

    def save(self):
        self.collection.insert_one({
            'id': self.id.lower(),
            'titleKr': self.titleKr.lower(),
            'releasedAt': self.releasedAt.lower(),
            'posterImageUrl': self.posterImageUrl.lower(),
            'mediaType': self.mediaType.lower()
        })

    @classmethod
    def get_all_movies(cls):
        movies = cls.collection.find({}, {'id': 1, 'posterImageUrl': 1, 'titleKr': 1, 'releasedAt': 1, 'mediaType': 1})
        return movies


# Define OTT platform classes
class AppleMovie(OTTMovie):
    collection = ott_db['Apple']

class CineFoxMovie(OTTMovie):
    collection = ott_db['CineFox']

class CoupangMovie(OTTMovie):
    collection = ott_db['Coupang']

class DisneyMovie(OTTMovie):
    collection = ott_db['Disney']

class GoogleMovie(OTTMovie):
    collection = ott_db['Google']

class LaftelMovie(OTTMovie):
    collection = ott_db['Laftel']

class NaverMovie(OTTMovie):
    collection = ott_db['Serieson']

class NetflixMovie(OTTMovie):
    collection = ott_db['Netflix']

class PrimevideoMovie(OTTMovie):
    collection = ott_db['Primevideo']

class TvingMovie(OTTMovie):
    collection = ott_db['Tving']

class UPlusMovie(OTTMovie):
    collection = ott_db['UPlus']

class WatchaMovie(OTTMovie):
    collection = ott_db['Watcha']

class WavveMovie(OTTMovie):
    collection = ott_db['Wavve']




class OTTdetail:
    collection = None

    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType):
        self.id = id
        self.titleKr = titleKr
        self.releasedAt = releasedAt
        self.posterImageUrl = posterImageUrl
        self.mediaType = mediaType

    def save(self):
        self.collection.insert_one({
            'id': self.id.lower(),
            'titleKr': self.titleKr.lower(),
            'releasedAt': self.releasedAt.lower(),
            'posterImageUrl': self.posterImageUrl.lower(),
            'mediaType': self.mediaType.lower()
        })

    @classmethod
    def get_all_movies(cls):
        movies = cls.collection.find({}, {'id': 1, 'posterImageUrl': 1, 'titleKr': 1, 'releasedAt': 1, 'mediaType': 1})
        
        return movies


# ott 중복제거한 db에서 detail을 보여주기 위한 클래스
from pymongo import MongoClient
import json
class OTT_detail:
    collection = ott_all_db.all

    @classmethod
    def get_collection(cls):
        return ott_all_db

    @classmethod
    def get_movie_by_id(cls, id):
        collection = cls.get_collection().all  # ott_db에서 컬렉션 이름 목록 가져오기
        document = collection.find_one({'id': str(id)})
        print(document)
        return document


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


from django.db import models
from django.utils import timezone

class MovieModel(models.Model):
    # 필요한 필드들을 정의합니다.
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    runtime = models.IntegerField()
    poster_path = models.URLField()
    genres = models.CharField(max_length=200)
    overview = models.TextField()

    def __str__(self):
        return self.title

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written')
    review = models.TextField(default="작성된 리뷰가 없습니다.")
    movie = models.ForeignKey(MovieModel, on_delete=models.CASCADE, related_name='reviews')

    timestamp = models.DateTimeField(default=timezone.now)
    liker = models.ManyToManyField(User, related_name='liked_reviews')
    updated_at = models.DateTimeField(null=True, blank=True)
    movie_rating = models.ForeignKey(MovieRating, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')

    # 나머지 코드...


    def __str__(self):
        return str(self.review)

    def save(self, *args, **kwargs):
        try:
            movie_rating = MovieRating.objects.get(user=self.user, movie_title=self.movie.title)  # MovieModel의 title을 사용하여 MovieRating 조회
        except MovieRating.DoesNotExist:
            movie_rating = MovieRating.objects.create(user=self.user, movie_title=self.movie.title, rating=None)
        
        self.movie_rating = movie_rating
        
        if self.pk is not None:
            self.updated_at = timezone.now()
        
        super().save(*args, **kwargs)