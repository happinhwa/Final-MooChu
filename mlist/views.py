from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime
from .utils import render_paginator_buttons
from django.http import HttpResponse
from django.shortcuts import render
from django.http import JsonResponse
from .models import AppleMovie, CineFoxMovie, CoupangMovie, DisneyMovie, GoogleMovie, LaftelMovie, NaverMovie, NetflixMovie, PrimevideoMovie, TvingMovie, UPlusMovie, WatchaMovie, WavveMovie, DNetflixMovie, DWatchaMovie, CMovie
from django.core.paginator import Paginator

def movielist(request):
    movies = list(Movie.collection.find())
    return render(request, 'mlist/movie_list.html', {'movies': movies})

# 영화 디테일 관련부분tmdb 기준임
from .models import Movie

def moviedetail(request, id):
    movie = Movie.get_movie_by_id(id)
    if movie:
        poster_url = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/' + movie.poster_path
        return render(request, 'mlist/movie_detail.html', {'movie': movie, 'poster_url': poster_url})
    else:
        return HttpResponse('Movie not found')

def ott_movie_list(request, ott):
    movie_data = []
    
    if ott == 'Apple':
        movies = AppleMovie.collection.find({})
    elif ott == 'CineFox':
        movies = CineFoxMovie.collection.find({})
    elif ott == 'Coupang':
        movies = CoupangMovie.collection.find({})
    elif ott == 'Disney':
        movies = DisneyMovie.collection.find({})
    elif ott == 'Google':
        movies = GoogleMovie.collection.find({})
    elif ott == 'Laftel':
        movies = LaftelMovie.collection.find({})
    elif ott == 'Naver':
        movies = NaverMovie.collection.find({})
    elif ott == 'Netflix':
        movies = NetflixMovie.collection.find({})
    elif ott == 'Primevideo':
        movies = PrimevideoMovie.collection.find({})
    elif ott == 'Tving':
        movies = TvingMovie.collection.find({})
    elif ott == 'UPlus':
        movies = UPlusMovie.collection.find({})
    elif ott == 'Watcha':
        movies = WatchaMovie.collection.find({})
    elif ott == 'Wavve':
        movies = WavveMovie.collection.find({})
    else:
        movies = Movie.collection.find({})  # ott 값이 없을 경우 전체 영화 데이터를 가져옵니다.
        
    for movie in movies:
        movie_data.append({
            'id': str(movie['_id']),  # Convert the movie's ObjectId value to a string and append it with the 'id' key.
            'posterImageUrl': movie['posterImageUrl'],
            'titleKr': movie['titleKr']
    })
        
        
    paginator = Paginator(movie_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'ott': ott,
        'movies': page_obj
    }
    
    return render(request, 'mlist/movie_list.html', context)

from django.shortcuts import render
from bson import ObjectId
from django.http import Http404
from bson.errors import InvalidId

def movie_detail_by_id(request, id):
    try:
        movie_id = ObjectId(str(id))

        # Determine OTT based on movie ID.
        ott = determine_ott(movie_id) # Implement logic to determine OTT based on movie ID.

        if ott == 'Apple':
            movie = AppleMovie.collection.find_one({'_id': movie_id})
        elif ott == 'CineFox':
            movie = CineFoxMovie.collection.find_one({'_id': movie_id})
        elif ott == 'Coupang':
            movie = CoupangMovie.collection.find_one({'_id': movie_id})
        elif ott == 'Disney':
            movie = DisneyMovie.collection.find_one({'_id': movie_id})
        elif ott == 'Google':
            movie = GoogleMovie.collection.find_one({'_id': movie_id})
        elif ott == 'Laftel':
            movie = LaftelMovie.collection.find_one({'_id': movie_id})
        elif ott == 'Naver':
            movie = NaverMovie.collection.find_one({'_id': movie_id})
        elif ott == 'Netflix':
            movie = NetflixMovie.collection.find_one({'_id': movie_id})
        elif ott == 'Primevideo':
            movie = PrimevideoMovie.collection.find_one({'_id': movie_id})
        elif ott == 'Tving':
            movie = TvingMovie.collection.find_one({'_id': movie_id})
        elif ott == 'UPlus':
            movie = UPlusMovie.collection.find_one({'_id': movie_id})
        elif ott == 'Watcha':
            movie = WatchaMovie.collection.find_one({'_id': movie_id})
        elif ott == 'Wavve':
            movie = WavveMovie.collection.find_one({'_id': movie_id})
        else:
            movie = None

        if movie:
            context = {
                'movie': {
                    'titleKr': movie['titleKr'],
                    'titleEn': movie['titleEn'],
                    'posterImageUrl': movie['posterImageUrl'],
                    'mediaType': movie['mediaType'],
                    'releasedAt': movie['releasedAt'],
                }
            }
            return render(request, 'mlist/movie_detail2.html', context)
        else:
            raise Http404('Could not find a movie.') # If no movie was found with that ID

    except InvalidId:
        raise Http404('Invalid ID.') # Handle if an invalid ID is provided

# 영화 세부정보 뷰
from django.shortcuts import render
from .models import OTT_detail

def movie_detail2(request, id):
    movie = OTT_detail.get_movie_by_id(id) # db에서 id를 기준으로 해당 값을
    print(movie)
    return render(request, 'mlist/movie_detail2.html', {'movie': movie})














#def moviedetail(request, id):

#
def determine_ott(movie_id):
    # 영화 ID를 기반으로 OTT를 결정하기 위한 로직을 구현합니다.
    # - 각 OTT 컬렉션에서 영화를 쿼리하고 movie_id의 존재 여부를 확인합니다.
    # - 각 OTT 컬렉션에서 movie_id의 존재 여부에 따라 OTT를 반환합니다.
    if AppleMovie.collection.find_one({'_id': movie_id}):
        return 'Apple'
    elif CineFoxMovie.collection.find_one({'_id': movie_id}):
        return 'CineFox'
    elif CoupangMovie.collection.find_one({'_id': movie_id}):
        return 'Coupang'
    elif DisneyMovie.collection.find_one({'_id': movie_id}):
        return 'Disney'
    elif GoogleMovie.collection.find_one({'_id': movie_id}):
        return 'Google'
    elif LaftelMovie.collection.find_one({'_id': movie_id}):
        return 'Laftel'
    elif NaverMovie.collection.find_one({'_id': movie_id}):
        return 'Naver'
    elif NetflixMovie.collection.find_one({'_id': movie_id}):
        return 'Netflix'
    elif PrimevideoMovie.collection.find_one({'_id': movie_id}):
        return 'Primevideo'
    elif TvingMovie.collection.find_one({'_id': movie_id}):
        return 'Tving'
    elif UPlusMovie.collection.find_one({'_id': movie_id}):
        return 'UPlus'
    elif WatchaMovie.collection.find_one({'_id': movie_id}):
        return 'Watcha'
    elif WavveMovie.collection.find_one({'_id': movie_id}):
        return 'Wavve'
    else:
        return None



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

#개봉예정작 관련 부분
import json

def c_net(request):
    netflix_movies = DNetflixMovie.get_all_movies()
    watcha_movies = DWatchaMovie.get_all_movies()

    movies = []

    for movie in netflix_movies:
        movie_obj = CMovie(movie)
        movie_obj.source = 'Netflix'
        movie_obj.num = movie.get('num')
        movie_obj.logo_image = '/images/N_logo.png'  # Update the logo image path
        movies.append(movie_obj)

    for movie in watcha_movies:
        movie_obj = CMovie(movie)
        movie_obj.source = 'Watcha'
        movie_obj.num = movie.get('num')
        movie_obj.logo_image = '/images/W_logo.png'  # Update the logo image path
        movies.append(movie_obj)

    # Group movies by dday
    dday_groups = {}
    for movie in movies:
        dday = movie.num
        if dday in dday_groups:
            dday_groups[dday].append(movie)
        else:
            dday_groups[dday] = [movie]

    # Sort the dday groups by dday in ascending order
    sorted_groups = sorted(dday_groups.items(), key=lambda x: x[0])

    # Pagination settings
    per_page = 20  # Set a maximum of 20 movies per page
    page_number = request.GET.get('page', 1)
    paginator = Paginator(sorted_groups, per_page)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'mlist/c_movie.html', context)
