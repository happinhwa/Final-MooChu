from django.shortcuts import render
from .models import Movie
from django.http import JsonResponse
from .models import ALL, AppleMovie, CineFoxMovie, CoupangMovie, DisneyMovie, GoogleMovie, LaftelMovie, NaverMovie, NetflixMovie, PrimevideoMovie, TvingMovie, UPlusMovie, WatchaMovie, WavveMovie
from django.core.paginator import Paginator
import gzip
import bson
from .models import CompressedDocument
import json

def movielist(request):
    movie_data1 = []
    all_movies = ALL.collection.find({})
    for all_movie in all_movies:
        poster_url = all_movie.get('posterImageUrl')
        if poster_url:
            urls = list(poster_url.values())
            movie_data1.extend(urls)
    
    paginator = Paginator(movie_data1, 10)  # 페이지당 10개씩 영화 목록을 보여줍니다.
    page_number = request.GET.get('page')  # 현재 페이지 번호를 가져옵니다.
    page_obj = paginator.get_page(page_number)  # 현재 페이지에 해당하는 영화 목록을 가져옵니다.
    
    context = {
        'movies': page_obj,
    }
    # print(movie_data1)
    return render(request, 'api/movielist.html', context)

def ott_movie_list(request, ott):
    movie_data = []
    genres = ['SF', '가족', '공연', '공포(호러)', '다큐멘터리', '드라마', '멜로/로맨스', '뮤지컬', '미스터리', '범죄',
              '서부극(웨스턴)', '서사', '서스펜스', '성인', '스릴러', '시사/교양', '애니메이션', '액션', '어드벤처(모험)',
              '예능', '음악', '전쟁', '코미디', '키즈', '판타지']
            
    if ott == 'ALL':
        movies = ALL.collection.find({})
        for movie in movies:
            poster_url = movie.get('posterImageUrl')
            if poster_url:
                urls = list(poster_url.values())
                movie_data.extend(urls)
        print(movie_data)
    
    elif ott == 'Apple':
        movies = AppleMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'CineFox':
        movies = CineFoxMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'Coupang':
        movies = CoupangMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'Disney':
        movies = DisneyMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'Google':
        movies = GoogleMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'Laftel':
        movies = LaftelMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'Naver':
        movies = NaverMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'Netflix':
        movies = NetflixMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'Primevideo':
        movies = PrimevideoMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'Tving':
        movies = TvingMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'UPlus':
        movies = UPlusMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'Watcha':
        movies = WatchaMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    elif ott == 'Wavve':
        movies = WavveMovie.collection.find({})
        for movie in movies:
            movie_data.append(movie['posterImageUrl'])
            
    else:
        movies = Movie.collection.find({})  # ott 값이 없을 경우 전체 영화 데이터를 가져옵니다.
        
    paginator = Paginator(movie_data, 10)  # 페이지당 10개씩 영화 목록을 보여줍니다.
    page_number = request.GET.get('page')  # 현재 페이지 번호를 가져옵니다.
    page_obj = paginator.get_page(page_number)  # 현재 페이지에 해당하는 영화 목록을 가져옵니다.
    
    context = {
        'ott': ott,
        'movies': page_obj,
        'genres': genres
    }
    return render(request, 'api/movielist.html', context)

from django.http import JsonResponse

def load_more_data(request):
    # 데이터를 가져오는 로직 구현
    movies = Movie.collection.find({})

    # JSON 형식으로 데이터 반환
    data = {
        'movies': [
            {
                'posterImageUrl': movie['posterImageUrl'],
                'title': movie['title'],
            }
            for movie in movies
        ]
    }
    return JsonResponse(data)


# def genre_filter(request, ott):
#     selected_genres = request.GET.getlist('genre')  # 선택된 장르들을 리스트로 가져옵니다.
#     movies = AppleMovie.collection.find({})
#     # OTT별로 해당하는 영화 컬렉션을 선택합니다.
#     if ott == 'Apple':
#         collection = AppleMovie.collection
#     elif ott == 'CineFox':
#         collection = CineFoxMovie.collection
#     elif ott == 'Coupang':
#         collection = CoupangMovie.collection
#     elif ott == 'Disney':
#         collection = DisneyMovie.collection
#     elif ott == 'Google':
#         collection = GoogleMovie.collection
#     elif ott == 'Laftel':
#         collection = LaftelMovie.collection
#     elif ott == 'Naver':
#         collection = NaverMovie.collection
#     elif ott == 'Netflix':
#         collection = NetflixMovie.collection
#     elif ott == 'Primevideo':
#         collection = PrimevideoMovie.collection
#     elif ott == 'Tving':
#         collection = TvingMovie.collection
#     elif ott == 'UPlus':
#         collection = UPlusMovie.collection
#     elif ott == 'Watcha':
#         collection = WatchaMovie.collection
#     elif ott == 'Wavve':
#         collection = WavveMovie.collection
#     else:
#         collection = Movie.collection  # ott 값이 없을 경우 전체 영화 데이터를 가져옵니다.

#     # 선택된 장르에 해당하는 영화를 필터링합니다.
#     movies = list(collection.find({'genre': {'$in': selected_genres}}))

#     context = {'movies': movies}
#     return render(request, 'api/movielist.html', context)

def genre_filter(request, ott):
    # 선택된 장르들을 가져옵니다.
    selected_genres = request.GET.getlist('genre')

    # 체크박스로 표시할 장르 리스트
    genres = [
        '가족', '공연', '공포(호러)', '다큐멘터리', '드라마', '멜로/로맨스', '뮤지컬', '미스터리',
        '범죄', '서부극(웨스턴)', '서사', '서스펜스', '성인', '스릴러', '시사/교양', '애니메이션',
        '액션', '어드벤처(모험)', '예능', '음악', '전쟁', '코미디', '키즈', '판타지'
    ]

    context = {
        'genres': genres,
        'selected_genres': selected_genres
    }

    return render(request, 'api/movielist.html', context)


    # else:
    #     movies = Movie.collection.find({})  # ott 값이 없을 경우 전체 영화 데이터를 가져옵니다.

    # return render(request, 'api/movielist.html', {'movies': movies})
