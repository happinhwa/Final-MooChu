from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bson import ObjectId
from django.http import Http404, JsonResponse

from .models import (
    AppleMovie, CineFoxMovie, CoupangMovie, DisneyMovie, GoogleMovie, LaftelMovie,
    NaverMovie, NetflixMovie, PrimevideoMovie, TvingMovie, UPlusMovie, WatchaMovie,
    WavveMovie, DNetflixMovie, DWatchaMovie, CMovie, Movie, OTT_detail
)
from .utils import render_paginator_buttons
from django.shortcuts import render, redirect
from .forms import ReviewForm
from review.models import Review
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse


from django.http import JsonResponse
from django.views.decorators.http import require_POST


from common.models import MovieRating
def movielist(request):
    movies = list(Movie.collection.find())
    return render(request, 'mlist/movie_list.html', {'movies': movies})


def moviedetail(request, id):
    movie = Movie.get_movie_by_id(id)
    if movie:
        poster_url = 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/' + movie.poster_path
        return render(request, 'mlist/movie_detail.html', {'movie': movie, 'poster_url': poster_url})
    else:
        return HttpResponse('Movie not found')


def ott_movie_list(request, ott):
    ott_movies = {
        'Apple': AppleMovie,
        'CineFox': CineFoxMovie,
        'Coupang': CoupangMovie,
        'Disney': DisneyMovie,
        'Google': GoogleMovie,
        'Laftel': LaftelMovie,
        'Naver': NaverMovie,
        'Netflix': NetflixMovie,
        'Primevideo': PrimevideoMovie,
        'Tving': TvingMovie,
        'UPlus': UPlusMovie,
        'Watcha': WatchaMovie,
        'Wavve': WavveMovie,
    }

    if ott in ott_movies:
        movies = ott_movies[ott].collection.find({})
    else:
        movies = Movie.collection.find({})

    movie_data = [
        {
            'id': str(movie['_id']),
            'posterImageUrl': movie['posterImageUrl'],
            'titleKr': movie['titleKr'],
        }
        for movie in movies
    ]

    paginator = Paginator(movie_data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'ott': ott,
        'movies': page_obj,
    }

    return render(request, 'mlist/movie_list.html', context)


def movie_detail_by_id(request, id):
    try:
        movie_id = ObjectId(str(id))
        ott = determine_ott(movie_id)

        ott_movies = {
            'Apple': AppleMovie,
            'CineFox': CineFoxMovie,
            'Coupang': CoupangMovie,
            'Disney': DisneyMovie,
            'Google': GoogleMovie,
            'Laftel': LaftelMovie,
            'Naver': NaverMovie,
            'Netflix': NetflixMovie,
            'Primevideo': PrimevideoMovie,
            'Tving': TvingMovie,
            'UPlus': UPlusMovie,
            'Watcha': WatchaMovie,
            'Wavve': WavveMovie,
        }

        if ott in ott_movies:
            movie = ott_movies[ott].collection.find_one({'_id': movie_id})
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
            return render(request, 'mlist/movie_detail.html', context)
        else:
            raise Http404('Could not find a movie.')

    except : #InvalidId
        raise Http404('Invalid ID.')


def determine_ott(movie_id):
    ott_movies = {
        'Apple': AppleMovie,
        'CineFox': CineFoxMovie,
        'Coupang': CoupangMovie,
        'Disney': DisneyMovie,
        'Google': GoogleMovie,
        'Laftel': LaftelMovie,
        'Naver': NaverMovie,
        'Netflix': NetflixMovie,
        'Primevideo': PrimevideoMovie,
        'Tving': TvingMovie,
        'UPlus': UPlusMovie,
        'Watcha': WatchaMovie,
        'Wavve': WavveMovie,
    }

    for ott, movie_cls in ott_movies.items():
        if movie_cls.collection.find_one({'_id': movie_id}):
            return ott

    return None


def load_more_data(request):
    movies = Movie.collection.find({})

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

# 개봉예정작 관련
def c_net(request):
    netflix_movies = DNetflixMovie.get_all_movies()
    watcha_movies = DWatchaMovie.get_all_movies()

    movies = []

    for movie in netflix_movies:
        movie_obj = CMovie(movie)
        movie_obj.source = 'Netflix'
        movie_obj.num = movie.get('num')
        movie_obj.logo_image = '/static/images/N_logo.png'  # Netflix 영화에 대한 로고 이미지 경로 업데이트

        movies.append(movie_obj)

    for movie in watcha_movies:
        movie_obj = CMovie(movie)
        movie_obj.source = 'Watcha'
        movie_obj.num = movie.get('num')
        movie_obj.logo_image = '/static/images/W_logo.png'  # Watcha 영화에 대한 로고 이미지 경로 업데이트
        movies.append(movie_obj)

    dday_groups = {}
    for movie in movies:
        dday = movie.num
        if dday in dday_groups:
            dday_groups[dday].append(movie)
        else:
            dday_groups[dday] = [movie]

    sorted_groups = sorted(dday_groups.items(), key=lambda x: x[0])

    per_page = 20
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


def movie_detail(request, id):
    movie = OTT_detail.get_movie_by_id(id)
    if movie:
        # Add review functionality
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                # Set the necessary movie details in the review
                review.movie_id = id
                review.save()
                return redirect('mlist:movie_detail', id=id)
        else:
            form = ReviewForm()

        return render(request, 'mlist/movie_detail.html', {'movie': movie, 'form': form})
    else:
        return redirect('movie_not_found')
    
    
    
################찜, 평점 관련##############
    
from django.shortcuts import render, redirect
from .models import Movie, MyList,OTT_detail
from .models import OTT_detail  # OTT_detail 클래스가 정의된 파일을 import

@login_required
def add_to_mylist(request, movie_id):
    ott_movie = OTT_detail.get_movie_by_id(movie_id)

    if ott_movie:
        # 이미 해당 영화가 찜 목록에 있는지 확인
        if not MyList.objects.filter(user=request.user, movie_id=movie_id).exists():
            movie = Movie.objects.create(
                id=str(movie_id),
                title=ott_movie.get('title', ''),
                poster_url=ott_movie.get('poster_url', ''),
                # 필요한 다른 영화 정보들도 추가할 수 있습니다.
            )
            MyList.objects.create(user=request.user, movie=movie)

    return redirect('movie_detail', movie_id=movie_id)
