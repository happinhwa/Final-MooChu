from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bson import ObjectId
from django.http import Http404, JsonResponse,HttpResponse

from .models import Media
from .utils import render_paginator_buttons
from collections import OrderedDict
# Create your views here.



## mainpage 함수
def mainpage(request):
    return render(request, 'moochu/mainpage.html')



# 페이징을 위한 호출 함수
def data_change(request,data):
    data =[
        {
            'id': str(movie['_id']),
            'posterImageUrl': movie['poster_image_url'],
            'titleKr': movie['title_kr'],
        }
        for movie in data
    ]

    paginator = Paginator(data, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj


def ott_media_list(request, ott, media_type):
    ott_service = ['ALL', 'Netflix', 'Wavve', 'Disney', 'Tving', 'Apple','CineFox', 'Watcha', 'Google', 'Laftel', 'Naver', 'Primevideo', 'UPlus']

    genres=['SF', '가족', '공연', '공포(호러)', '다큐멘터리', '드라마', '멜로/로맨스', '뮤지컬', '미스터리', '범죄',
                   '서부극(웨스턴)', '서사', '서스펜스', '성인', '스릴러', '시사/교양', '애니메이션', '액션', '어드벤처(모험)',
                   '예능', '음악', '전쟁', '코미디', '키즈', '판타지']
    
    if ott=='ALL':
        data = list(Media.collection.find({"media_type": media_type}, {"poster_image_url": 1, "title_kr": 1}))

        ## 제목으로 중복 제거를 위한 로직
        unique_movies = OrderedDict()
        for movie in data:
            if movie['title_kr'] not in unique_movies:
                unique_movies[movie['title_kr']] = movie
        
        data = list(unique_movies.values())
    else:
        data = list(Media.collection.find({"OTT":ott, "media_type":media_type}, {"poster_image_url": 1, "title_kr": 1}))

    
    page_obj= data_change(request,data)

    context = {
        'ott': ott,
        'data': page_obj,
        'genres' : genres,
        'type':media_type,
        'ott_service':ott_service
    }

    return render(request, 'moochu/movie_list.html', context)


def genre_filter(request, ott, media_type):
    ott_service = ['ALL', 'Netflix', 'Wavve', 'Disney', 'Tving', 'Apple','CineFox', 'Watcha', 'Google', 'Laftel', 'Naver', 'Primevideo', 'UPlus']
    genres=['SF', '가족', '공연', '공포(호러)', '다큐멘터리', '드라마', '멜로/로맨스', '뮤지컬', '미스터리', '범죄',
                   '서부극(웨스턴)', '서사', '서스펜스', '성인', '스릴러', '시사/교양', '애니메이션', '액션', '어드벤처(모험)',
                   '예능', '음악', '전쟁', '코미디', '키즈', '판타지']
    
    # 선택된 장르들을 가져옵니다.
    selected_genres = request.GET.getlist('genres')

    # 선택된 장르에 해당하는 영화를 필터링합니다.
    if ott=='ALL':
        data = list(Media.collection.find({"genres": {"$elemMatch": {"$in": selected_genres}}, "media_type":media_type}))
        ## 제목으로 중복 제거를 위한 로직
        unique_movies = OrderedDict()
        for movie in data:
            if movie['title_kr'] not in unique_movies:
                unique_movies[movie['title_kr']] = movie
        
        data = list(unique_movies.values())
    else:
        data = list(Media.collection.find({"genres": {"$elemMatch": {"$in": selected_genres}}, "media_type":media_type, 'OTT':ott }))



    page_obj= data_change(request,data)

    context = {
        'ott': ott,
        'data': page_obj,
        'genres' : genres,
        'selected_genres': selected_genres,
        'type':media_type,
        'ott_service':ott_service
    }

    return render(request, 'moochu/movie_list.html', context)


# 영화 상세 페이지 
def movie_detail(request, movie_id):
    ## TV 또는 MOVIE에 맞게 media 리스트 저장
    data = list(Media.collection.find({"_id": ObjectId(movie_id)}))
    ## 필요한 데이터 형식으로 변형
    data =[
        {
            'id': str(movie['_id']),
            'posterImageUrl': movie['poster_image_url'],
            'titleKr': movie['title_kr'],
            'age' : movie['rating'],
            'genre' : movie['genres'],
            'synopsis' : movie['synopsis'],
            'date' : movie['released_At'],
        }
        for movie in data
    ]

    context = {
            'movie': data[0],
        }

    return render(request, 'moochu/media_detail.html', context)





