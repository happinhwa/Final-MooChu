from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bson import ObjectId
from django.http import Http404, JsonResponse,HttpResponse
from django.db.models import Avg
from common.models import MovieRating
from review.models import Review
from .models import Media
from .utils import render_paginator_buttons
from collections import OrderedDict
# Create your views here.



## mainpage 함수
def mainpage(request):
    num=[2,3,4,5,6,7,8,9,10]
    context={"num":num,}
    return render(request, 'moochu/mainpage.html', context)
    


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
    ott_service = ['All', 'Netflix', 'Tving', 'Watcha', 'CoupangPlay', 'Wavve', 'Disney', 'Apple', 'Google', 'Laftel', 'Naver', 'Primevideo', 'UPlus', 'CineFox']

    genres=['SF', '가족', '공연', '공포(호러)', '다큐멘터리', '드라마', '멜로/로맨스', '뮤지컬', '미스터리', '범죄',
                   '서부극(웨스턴)', '서사', '서스펜스', '성인', '스릴러', '시사/교양', '애니메이션', '액션', '어드벤처(모험)',
                   '예능', '음악', '전쟁', '코미디', '키즈', '판타지']
    
    if ott=='All':
        pipeline = [
            {"$match": {"media_type": media_type, "indexRating.score": {"$gte": 73.2}}},
            {"$sample": {"size": 1000}}  # 임시로 충분히 큰 숫자를 지정해 무작위 순서로 문서들을 반환받는다.
        ]

        movies = Media.collection.aggregate(pipeline)

        # 중복제거
        unique_movies = OrderedDict()
        for movie in movies:
            if movie['title_kr'] not in unique_movies:
                unique_movies[movie['title_kr']] = movie
        data = list(unique_movies.values())
        
    else:
        pipeline = [
            {"$match": {"media_type": media_type,"OTT":ott, "indexRating.score": {"$gte": 73.2}}},
            {"$sample": {"size": 1000}}  # 임시로 충분히 큰 숫자를 지정해 무작위 순서로 문서들을 반환받는다.
        ]

        data = Media.collection.aggregate(pipeline)

    
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
    ott_service = ['All', 'Netflix', 'Tving', 'Watcha', 'CoupangPlay', 'Wavve', 'Disney', 'Apple', 'Google', 'Laftel', 'Naver', 'Primevideo', 'UPlus', 'CineFox']

    genres=['SF', '가족', '공연', '공포(호러)', '다큐멘터리', '드라마', '멜로/로맨스', '뮤지컬', '미스터리', '범죄',
                   '서부극(웨스턴)', '서사', '서스펜스', '성인', '스릴러', '시사/교양', '애니메이션', '액션', '어드벤처(모험)',
                   '예능', '음악', '전쟁', '코미디', '키즈', '판타지']
    
    # 선택된 장르들을 가져옵니다.
    selected_genres = request.GET.getlist('genres')

    # 선택된 장르에 해당하는 영화를 필터링합니다.
    if ott=='All':
        pipeline = [
            {"$match": {"genres": {"$elemMatch": {"$in": selected_genres}}, "indexRating.score": {"$gte": 73.2}}},
            {"$sample": {"size": 1000}}  # 임시로 충분히 큰 숫자를 지정해 무작위 순서로 문서들을 반환받는다.
        ]


        movies = Media.collection.aggregate(pipeline)
         # 중복제거
        unique_movies = OrderedDict()
        for movie in movies:
            if movie['title_kr'] not in unique_movies:
                unique_movies[movie['title_kr']] = movie
        data = list(unique_movies.values())
    else:
        pipeline = [
            {"$match": {"genres": {"$elemMatch": {"$in": selected_genres}}, "indexRating.score": {"$gte": 73.2}}},
            {"$sample": {"size": 1000}}  # 임시로 충분히 큰 숫자를 지정해 무작위 순서로 문서들을 반환받는다.
        ]


        data = Media.collection.aggregate(pipeline)



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

    average_rating = MovieRating.objects.filter(media_id=str(movie_id)).aggregate(Avg('rating'))['rating__avg']
    reviews = Review.objects.filter(media_id=str(movie_id)).order_by('-create_date')
    review_count = Review.objects.filter(media_id=str(movie_id)).count()
    context = {
            'movie': data[0],
            'average_rating': average_rating,
            'reviews': reviews,
            'review_count': review_count,
        }

    return render(request, 'moochu/media_detail.html', context)





