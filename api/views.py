from django.shortcuts import render
from .models import Movie
from django.http import JsonResponse
from .models import AppleMovie, CineFoxMovie, CoupangMovie, DisneyMovie, GoogleMovie, LaftelMovie, NaverMovie, NetflixMovie, PrimevideoMovie, TvingMovie, UPlusMovie, WatchaMovie, WavveMovie
from django.core.paginator import Paginator

def movielist(request):
    movies = Movie.collection.find({})
    return render(request, 'api/movielist.html', {'movies': movies})


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
        
    paginator = Paginator(movie_data, 10)  # 페이지당 10개씩 영화 목록을 보여줍니다.
    page_number = request.GET.get('page')  # 현재 페이지 번호를 가져옵니다.
    page_obj = paginator.get_page(page_number)  # 현재 페이지에 해당하는 영화 목록을 가져옵니다.
    
    context = {
        'ott': ott,
        'movies': page_obj
    }
    print(type(movie_data))
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


def genre_filter(request, genre):
    movies = Movie.objects.filter(genre=genre)
    context = {'movies': movies}
    return render(request, 'api/movielist.html', context)


    # else:
    #     movies = Movie.collection.find({})  # ott 값이 없을 경우 전체 영화 데이터를 가져옵니다.

    # return render(request, 'api/movielist.html', {'movies': movies})
