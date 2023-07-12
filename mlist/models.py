from django.db import models
from django.utils import timezone
from django.conf import settings
from pymongo import MongoClient


#DB설정하기
# TMDB 데이터베이스 연결 설정
MONGODB_URI = settings.MONGODB_URI
TMDB_MONGODB_NAME = settings.TMDB_MONGODB_NAME

# OTT 데이터베이스 연결 설정
OTT_MONGODB_NAME = settings.OTT_MONGODB_NAME

# OTT 전체 데이터베이스 연결 설정
OTT_ALLDB_NAME = settings.OTT_ALLDB_NAME

# 다음 데이터베이스 연결 설정
DAUM_MONGODB_NAME = settings.DAUM_MONGODB_NAME


# TMDB 데이터베이스 연결
mongo_client = MongoClient(MONGODB_URI) 
tmdb_db = mongo_client[TMDB_MONGODB_NAME]

# OTT 데이터베이스 연결
ott_db = mongo_client[OTT_MONGODB_NAME]
# OTT 중복제거한 데이터베이스 연결
ottall_db = mongo_client[OTT_ALLDB_NAME]
# daum 데이터베이스 연결
daum_db = mongo_client[DAUM_MONGODB_NAME]

#tmdb에서 가져오기
class Movie:
    collection = tmdb_db.movie
    @classmethod
    def get_collection(cls):
        return tmdb_db

    def __init__(self, id, title, release_date, runtime, poster_path, genres, overview):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.runtime = runtime
        self.poster_path = poster_path
        self.genres = genres
        self.overview = overview

    def save(self):
        collection = self.get_collection().movies
        collection.insert_one({
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'runtime': self.runtime,
            'poster_path': self.poster_path,
            'genres': self.genres,
            'overview': self.overview,
        })

    @classmethod
    def get_movie_by_id(cls, movie_id):
        tmdb_db = cls.get_collection()
        for collection_name in tmdb_db.list_collection_names():
            collection = tmdb_db[collection_name]
            movie = collection.find_one({'id': movie_id})
            if movie:
                genre_names = [genre['name'] for genre in movie['genres']]
                movie['genres'] = genre_names
                return Movie(
                    movie['id'],
                    movie['title'],
                    movie['release_date'],
                    movie['runtime'],
                    movie['poster_path'],
                    movie['genres'],
                    movie['overview'],
                )
        return None

#OTT별로 가져오기
class OTTMovie:
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
    
    
class AppleMovie(OTTMovie):
    collection = ott_db['Apple']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType,)


class CineFoxMovie(OTTMovie):
    collection = ott_db['CineFox']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )


class CoupangMovie(OTTMovie):
    collection = ott_db['Coupang']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )


class DisneyMovie(OTTMovie):
    collection = ott_db['Disney']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )


class GoogleMovie(OTTMovie):
    collection = ott_db['Google']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )


class LaftelMovie(OTTMovie):
    collection = ott_db['Laftel']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )


class NaverMovie(OTTMovie):
    collection = ott_db['Serieson']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )


class NetflixMovie(OTTMovie):
    collection = ott_db['Netflix']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )


class PrimevideoMovie(OTTMovie):
    collection = ott_db['Primevideo']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )


class TvingMovie(OTTMovie):
    collection = ott_db['Tving']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )


class UPlusMovie(OTTMovie):
    collection = ott_db['UPlus']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )


class WatchaMovie(OTTMovie):
    collection = ott_db['Watcha']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )


class WavveMovie(OTTMovie):
    collection = ott_db['Wavve']
    
    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
        super().__init__(id, titleKr, releasedAt, posterImageUrl, mediaType, )

    # OTTMovie 클래스에 특화된 메서드 추가
    # 필요한 기능을 구현해주세요.
# 연결 종료


class Ott_detail:
    collection = ottall_db.all
    
    @classmethod
    def get_collection(cls):
        return ottall_db

    def __init__(self, id, titleKr, releasedAt, runtime, posterImageUrl, mediaType, overview):
        self.id = id
        self.title = titleKr
        self.release_date = releasedAt
        self.runtime = runtime
        self.poster_url = posterImageUrl
        self.mediaType = mediaType
        self.overview = overview

    def save(self):
        collection = self.get_collection().movies
        collection.insert_one({
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'runtime': self.runtime,
            'poster_path': self.poster_url,
            'mediaType': self.mediaType,
            'overview': self.overview,
        })

    @classmethod
    def get_movie_by_id(cls, id):
        datail_db = cls.get_collection()
        for collection_name in datail_db.list_collection_names():
            collection = datail_db[collection_name]
            movie = collection.find_one({'id': id})
            if movie:
                genre_names = [genre['name'] for genre in movie['genres']]
                movie['genres'] = genre_names
                return Movie(
                    movie['id'],
                    movie['title'],
                    movie['release_date'],
                    movie['runtime'],
                    movie['poster_path'],
                    movie['genres'],
                    movie['overview'],
                )
        return None






class DaumMovie:
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
    
    def __init__(self, img_link):
        super().__init__(img_link)

    @classmethod
    def get_all_movies(cls):
        movies = cls.collection.find({}, {'num': 1, 'title': 1, 'img_link': 1})
        return list(movies)


class DWatchaMovie(DaumMovie):
    collection = daum_db['daumwatcha']
    
    def __init__(self, img_link):
        super().__init__(img_link)

    @classmethod
    def get_all_movies(cls):
        movies = cls.collection.find({}, {'num': 1, 'title': 1, 'img_link': 1})
        return list(movies)

# 영화관 추가시
#class Dtheater(DaumMovie):
#    collection = daum_db['daumtheater']
#    
#    def __init__(self, id, titleKr, releasedAt, posterImageUrl, mediaType, ):
#        super().__init__(posterImageUrl)
#

#
#tmdb_client.close()
#ott_client.close()
#daum_client.close()