from djongo import models as djongo_models
from django.db import models
from django.utils import timezone
from django.conf import settings
from pymongo import MongoClient

# TMDB 데이터베이스 연결 설정
TMDB_MONGODB_URI = settings.TMDB_MONGODB_URI
TMDB_MONGODB_NAME = settings.TMDB_MONGODB_NAME

# OTT 데이터베이스 연결 설정
OTT_MONGODB_URI = settings.OTT_MONGODB_URI
OTT_MONGODB_NAME = settings.OTT_MONGODB_NAME

# TMDB 데이터베이스 연결
tmdb_client = MongoClient(TMDB_MONGODB_URI)
tmdb_db = tmdb_client[TMDB_MONGODB_NAME]

# OTT 데이터베이스 연결
ott_client = MongoClient(OTT_MONGODB_URI)
ott_db = ott_client[OTT_MONGODB_NAME]

class Movie:
    collection = tmdb_db.movies

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def save(self):
        self.collection.insert_one({
            'title': self.title,
            'release_date': self.release_date
        })

    @classmethod
    def get_all_movies(cls):
        movies = cls.collection.find({}, {'_id': 0})
        return list(movies)


class OTTMovie:
    def __init__(self, posterImageUrl):
        self.posterImageUrl = posterImageUrl

    def save(self):
        self.collection.insert_one({
            'posterImageUrl': self.posterImageUrl.lower()
        })

    @classmethod
    def get_all_movies(cls):
        movies = cls.collection.find({}, {'_id': 0, 'posterImageUrl': 1})
        titles = [movie['posterImageUrl'] for movie in movies]
        return titles
    
class ALL(OTTMovie):
    collection = ott_db['OTT_SUM']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)
    
class AppleMovie(OTTMovie):
    collection = ott_db['Apple']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class CineFoxMovie(OTTMovie):
    collection = ott_db['CineFox']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class CoupangMovie(OTTMovie):
    collection = ott_db['Coupang']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class DisneyMovie(OTTMovie):
    collection = ott_db['Disney']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class GoogleMovie(OTTMovie):
    collection = ott_db['Google']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class LaftelMovie(OTTMovie):
    collection = ott_db['Laftel']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class NaverMovie(OTTMovie):
    collection = ott_db['Laftel']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class NetflixMovie(OTTMovie):
    collection = ott_db['Netflix']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class PrimevideoMovie(OTTMovie):
    collection = ott_db['Primevideo']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class TvingMovie(OTTMovie):
    collection = ott_db['Tving']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class UPlusMovie(OTTMovie):
    collection = ott_db['UPlus']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class WatchaMovie(OTTMovie):
    collection = ott_db['Watcha']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)


class WavveMovie(OTTMovie):
    collection = ott_db['Wavve']
    
    def __init__(self, posterImageUrl):
        super().__init__(posterImageUrl)

class CompressedDocument(models.Model):
    compressed_data = models.BinaryField()
    # OTTMovie 클래스에 특화된 메서드 추가
    # 필요한 기능을 구현해주세요.
# 연결 종료
tmdb_client.close()
ott_client.close()

