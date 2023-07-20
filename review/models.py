from django.db import models
from django.utils import timezone
from common.models import User, MovieRating
from django.conf import settings
from pymongo import MongoClient

from django.db import models
from django.utils import timezone
from common.models import User, MovieRating

from django.db import models
from mlist.models import Movie


# 일반적인 Django 모델로서, MongoDB의 데이터를 저장할 필요는 없습니다.
# MongoDB 연결
mongo_client = MongoClient(settings.MONGODB_URI)

# ott_all_db 데이터베이스 선택
ott_all_db = mongo_client[settings.OTT_ALLDB_NAME]

# 'all' 컬렉션에서 id 값만 가져오기
def get_all_ids_from_all_collection():
    all_collection = ott_all_db['all']
    ids = [doc['_id'] for doc in all_collection.find({}, {'_id': 1})]
    return ids

# Movie 클래스 정의
class Movie(models.Model):
    # id 필드를 primary key로 사용하고 CharField로 선언
    id = models.CharField(max_length=255, primary_key=True)

# MongoDB에서 가져온 id 값들을 Movie 객체로 변환하여 저장
def save_ids_to_movie_model():
    ids = get_all_ids_from_all_collection()
    for id in ids:
        movie = Movie(id=id)
        movie.save()

# 실행해서 id 값들을 Movie 객체로 저장
save_ids_to_movie_model()

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_writer')
    review = models.TextField(default="작성된 리뷰가 없습니다.")
    movie_id = models.IntegerField(default=1)  # MongoDB에서 가져온 id를 문자열로 저장
    rating = models.IntegerField(default=0)
    timestamp = models.DateTimeField(default=timezone.now)
    liker = models.ManyToManyField(User, related_name='review_liker')
    updated_at = models.DateTimeField(null=True, blank=True)
    movie_rating = models.ForeignKey(MovieRating, on_delete=models.SET_NULL, null=True, blank=True, related_name='review_Mrating')

    def __str__(self):
        return str(self.review)

    def save(self, *args, **kwargs):
        try:
            movie_rating = MovieRating.objects.get(user=self.user, movie_title=self.movie_id)
        except MovieRating.DoesNotExist:
            movie_rating = MovieRating.objects.create(user=self.user, movie_title=self.movie_id, rating=None)
        
        self.movie_rating = movie_rating
        
        if self.pk is not None:
            self.updated_at = timezone.now()
        
        super().save(*args, **kwargs)
        


#class Movie(models.Model):
#    genre = models.CharField(max_length=255)
#    release_date = models.DateField()
#    director = models.CharField(max_length=255)
#    cast = models.TextField()
#    synopsis = models.TextField(default="작성된 영화 줄거리가 없습니다.")
#    def __str__(self):
#        return str(self.title)
#    class Meta:
#        db_table = 'movie'
#        app_label = 'review'

#class Review(models.Model):
#    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_writer')
#
#    review = models.TextField(default="작성된 리뷰가 없습니다.")
#    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#    timestamp = models.DateTimeField(default=timezone.now)
#    liker = models.ManyToManyField(User, related_name='review_liker')
#    updated_at = models.DateTimeField(null=True, blank=True)
#    movie_rating = models.ForeignKey(MovieRating, on_delete=models.SET_NULL, null=True, blank=True, related_name='review_Mrating')
#    def __str__(self):
#        return str(self.review)
#
#    def save(self, *args, **kwargs):
#        try:
#
#            movie_rating = MovieRating.objects.get(user=self.user, movie_title=self.movie.title)
#        except MovieRating.DoesNotExist:
#            movie_rating = MovieRating.objects.create(user=self.user, movie_title=self.movie.title, rating=None)
#        
#        self.movie_rating = movie_rating
#        
#        if self.pk is not None:
#            self.updated_at = timezone.now()
#        
#        super().save(*args, **kwargs)
        
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
