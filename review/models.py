from django.db import models
from django.utils import timezone
from common.models import User, MovieRating
from django.conf import settings
from pymongo import MongoClient


mongo_client = MongoClient(settings.MONGODB_URI)

tmdb_db = mongo_client[settings.TMDB_MONGODB_NAME]
actor_db = mongo_client[settings.TMDB_MONGODB_ACTOR]
 
ott_db = mongo_client[settings.OTT_MONGODB_NAME]
ott_all_db = mongo_client[settings.OTT_ALLDB_NAME]

daum_db = mongo_client[settings.DAUM_MONGODB_NAME]




class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    release_date = models.DateField()
    director = models.CharField(max_length=255)
    cast = models.TextField()
    synopsis = models.TextField(default="작성된 영화 줄거리가 없습니다.")
    def __str__(self):
        return str(self.title)
    class Meta:
        db_table = 'movie'
        app_label = 'review'


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_writer')
    review = models.TextField(default="작성된 리뷰가 없습니다.")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    liker = models.ManyToManyField(User, related_name='review_liker')
    updated_at = models.DateTimeField(null=True, blank=True)
    movie_rating = models.ForeignKey(MovieRating, on_delete=models.SET_NULL, null=True, blank=True, related_name='review_Mrating')

    def __str__(self):
        return str(self.review)

    def save(self, *args, **kwargs):
        try:
            movie_rating = MovieRating.objects.get(user=self.user, movie_title=self.movie.title)
        except MovieRating.DoesNotExist:
            movie_rating = MovieRating.objects.create(user=self.user, movie_title=self.movie.title, rating=None)
        
        self.movie_rating = movie_rating
        
        if self.pk is not None:
            self.updated_at = timezone.now()
        
        super().save(*args, **kwargs)
        
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    comment_txt = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
  
    def __str__(self):
        return str(self.comment_txt)

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.updated_at = timezone.now() # 수정되었을 경우 updated_timestamp 필드를 업데이트합니다.
        super().save(*args, **kwargs)
        
        
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
        return document
