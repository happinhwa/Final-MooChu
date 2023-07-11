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

# OTT 데이터베이스 연결 설정
DAUM_MONGODB_URI = settings.DAUM_MONGODB_URI
DAUM_MONGODB_NAME = settings.DAUM_MONGODB_NAME


# TMDB 데이터베이스 연결
tmdb_client = MongoClient(TMDB_MONGODB_URI) 
tmdb_db = tmdb_client[TMDB_MONGODB_NAME]

# OTT 데이터베이스 연결
ott_client = MongoClient(OTT_MONGODB_URI)
ott_db = ott_client[OTT_MONGODB_NAME]
# daum 데이터베이스 연결
daum_client = MongoClient(DAUM_MONGODB_URI)
daum_db = daum_client[DAUM_MONGODB_NAME]

#tmdb에서 가져오기
class Movie:
    def __init__(self, id, title, release_date, runtime, poster_path, genres, overview):
        self.id = id
        self.title = title
        self.release_date = release_date
        self.runtime = runtime
        self.poster_path = poster_path
        self.genres = genres
        self.overview = overview

    def save(self):
        collection = tmdb_db.movies
        collection.insert_one({
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'runtime' : self.runtime,
            'poster_path' : self.poster_path,
            'genres' : self.genres,
            'overview' : self.overview,
        })

    @classmethod
    def get_movie_by_id(cls, movie_id):
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
    collection = ott_db['Serieson']
    
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

    # OTTMovie 클래스에 특화된 메서드 추가
    # 필요한 기능을 구현해주세요.
# 연결 종료


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
#    def __init__(self, posterImageUrl):
#        super().__init__(posterImageUrl)
#

#
#tmdb_client.close()
#ott_client.close()
#daum_client.close()