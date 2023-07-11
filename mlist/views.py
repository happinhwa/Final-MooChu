from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime
from .utils import render_paginator_buttons
from django.http import HttpResponse
from django.shortcuts import render
from .models import Movie
from django.http import JsonResponse
from .models import AppleMovie, CineFoxMovie, CoupangMovie, DisneyMovie, GoogleMovie, LaftelMovie, NaverMovie, NetflixMovie, PrimevideoMovie, TvingMovie, UPlusMovie, WatchaMovie, WavveMovie, DNetflixMovie, DWatchaMovie
from django.core.paginator import Paginator

def movielist(request):
    movies = list(Movie.collection.find())
    return render(request, 'mlist/movie_list.html', {'movies': movies})

# 영화 디테일 관련부분
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
        
    paginator = Paginator(movie_data, 20)  # 페이지당 10개씩 영화 목록을 보여줍니다.
    page_number = request.GET.get('page')  # 현재 페이지 번호를 가져옵니다.
    page_obj = paginator.get_page(page_number)  # 현재 페이지에 해당하는 영화 목록을 가져옵니다.
    
    context = {
        'ott': ott,
        'movies': page_obj
    }
    print(type(movie_data))
    return render(request, 'mlist/movie_list.html', context)

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


def genre_filter(request, genre):
    movies = Movie.objects.filter(genre=genre)
    context = {'movies': movies}
    return render(request, 'api/movielist.html', context)

#개봉예정작 관련 부분
import json

def c_net(request):
    movies = DNetflixMovie.get_all_movies()

    # Group movies by dday
    dday_groups = {}
    for movie in movies:
        dday = movie['num']
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


#
#
#
#
#
#
## 전체 페이지 보여주기
#def redirect_to_movie_list(request):
#    return redirect('mlist:mlist_page', page_number=1)
##페이지 1으로 바로 리다이렉트하기 위함.
#
#def movie_list(request, page_number=None):
#    if page_number is None:
#        page_number = int(request.GET.get('page', 1))
#
#    total_movies = collection.count_documents({})
#    per_page = 20
#
#    if page_number < 1:
#        page_number = 1
#
#    movies = collection.find({}, {"genres": 1, "title": 1, "poster_path": 1, "overview": 1, "release_date": 1})
#    movies = list(movies)
#    paginator = Paginator(movies, per_page)
#
#    try:
#        page_obj = paginator.page(page_number)
#    except PageNotAnInteger:
#        page_obj = paginator.page(1)
#    except EmptyPage:
#        page_obj = paginator.page(paginator.num_pages)
#
#    url = f"/mlist/page={page_number}/"
#    if request.GET.get('page') and int(request.GET['page']) != page_number:
#        return redirect(url)
#
#    paginator_buttons = render_paginator_buttons(paginator, page_number)
#
#    context = {
#        'movies': page_obj,
#        'page_obj': page_obj,
#        'total_movies': total_movies,
#        'paginator': paginator_buttons
#    }
#
#    return render(request, 'mlist/movie_list.html', context)
#
#
#
#
#
#
#from datetime import datetime
#
#def c_net(request):
#    movies = mongodb_collection1.find({}, {"num": 1, "title": 1, "img_link": 1})
#
#    # Group movies by dday
#    dday_groups = {}
#    for movie in movies:
#        dday = movie['num']
#        if dday in dday_groups:
#            dday_groups[dday].append(movie)
#        else:
#            dday_groups[dday] = [movie]
#
#    # Sort the dday groups by dday in ascending order
#    sorted_groups = sorted(dday_groups.items(), key=lambda x: x[0])
#
#    # Pagination settings
#    per_page = 20  # Set a maximum of 20 movies per page
#    page_number = request.GET.get('page', 1)
#    paginator = Paginator(sorted_groups, per_page)
#
#    try:
#        page_obj = paginator.page(page_number)
#    except PageNotAnInteger:
#        page_obj = paginator.page(1)
#    except EmptyPage:
#        page_obj = paginator.page(paginator.num_pages)
#
#    context = {
#        'page_obj': page_obj,
#    }
#    return render(request, 'mlist/c_movie.html', context)
#
#
#def render_paginator_buttons(paginator, current_page):
#    page_buttons = []
#    start_page = max(1, current_page - 2)
#    end_page = min(paginator.num_pages, current_page + 2)
#
#    if start_page > 1:
#        page_buttons.append((1, False))
#        if start_page > 2:
#            page_buttons.append((-1, False))
#
#    for page in range(start_page, end_page + 1):
#        is_current = (page == current_page)
#        page_buttons.append((page, is_current))
#
#    if end_page < paginator.num_pages:
#        if end_page < paginator.num_pages - 1:
#            page_buttons.append((-1, False))
#        page_buttons.append((paginator.num_pages, False))
#
#    return page_buttons
#