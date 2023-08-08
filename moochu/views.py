from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from bson import ObjectId
from django.http import Http404, JsonResponse,HttpResponse
from django.db.models import Avg
from common.models import MovieRating
from review.models import Review
from .models import Media
from collections import OrderedDict
import redis
import random

# Create your views here.
def convert_to_movie_dict(media_data):
    return {
        'id': str(media_data["_id"]),
        'title': media_data["title_kr"]
    }


## mainpage 함수
def mainpage(request):

    # Redis 클라이언트 생성
    r = redis.StrictRedis(host='34.22.93.125', port=6379, db=0)


                                                  ## 오늘의 영화 TOP10 데이터 
    # Redis에서 'popularity'에 해당하는 값을 가져옴
    value = r.zrevrange('popularity', 0, -1, withscores=True)

    # ByteArray를 디코드하여 문자열로 변환
    value = [(item[0].decode('utf-8'), item[1]) for item in value]

    # 첫 번째 값만 다른 변수에 저장
    top1 = list(value[0])
    data = Media.collection.find_one({'_id': ObjectId(top1[0])})
    reviews = Review.objects.filter(media_id=str(data['_id'])).order_by('-create_date')
    top1_review = reviews.first()
    top1 ={
            'id': str(data['_id']),
            'title': data['title_kr'],
            'synopsis': data['synopsis'],
        }
    
    # 나머지 값들은 value에 저장
    ranking = value[1:]
    top2=[]
    for media in ranking:
        data = Media.collection.find_one({'_id': ObjectId(media[0])})
        data ={
            'id': str(data['_id']),
            'title': data['title_kr'],
            'synopsis': data['synopsis']
        }
        
        top2.append(data)
    
                                                ## 최신 리뷰 데이터 들고오기 
    reviews = Review.objects.order_by('-create_date')
    combined_data = []

    for review in reviews:
        media_id = review.media_id
        media_data = Media.collection.find_one({'_id': ObjectId(media_id)})
        movie = convert_to_movie_dict(media_data)
        
        combined_review_movie_data = {
            'movie': movie,
            'review': review,
        }
        
        combined_data.append(combined_review_movie_data)
    


                                                ## 최근 본 미디어 데이터 
    value = r.lrange(str(request.user.id), 1, 10)

    value = [(item.decode('utf-8')) for item in value]
    print(value)
    recent=[]
    for media in value:
        data = Media.collection.find_one({'_id': ObjectId(media)})
        data ={
            'id': str(data['_id']),
            'title': data['title_kr'],
            'synopsis': data['synopsis']
        }
        
        recent.append(data)
                                                ## 추천 결과 미디어 랜덤으로 20개 
    try:
        r3 = redis.StrictRedis(host='34.22.93.125', port=6379, db=3)
        if r3.lrange(str(request.user.id), 1, 100):
            value = r3.lrange(str(request.user.id), 1, 100)
        else:
            r2 = redis.StrictRedis(host='34.22.93.125', port=6379, db=2)
            value = r2.lrange(str(request.user.id), 1, 100)


        # 랜덤하게 20개 선택
        items = random.sample(value, 20)
        recommendation = [(item.decode('utf-8')) for item in items]
    except:
        recommendation= None
    context = {"top1": top1,
               "top2": top2, 
               "reviews": reviews,
               'top1_review':top1_review,
               'combined_data':combined_data,
               'recent': recent,
                'recommendation':recommendation }
    
    
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

        data = Media.collection.aggregate(pipeline)

    else:
        pipeline = [
            {"$match": {"media_type": media_type,"OTT": {"$elemMatch": {"$in": ott}}, "indexRating.score": {"$gte": 73.2}}},
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

    if request.user.is_authenticated:
        user_review = Review.objects.filter(media_id=str(movie_id), writer=request.user).first()
    else:
        user_review = None

    context = {
            'movie': data[0],
            'average_rating': average_rating,
            'reviews': reviews,
            'review_count': review_count,
            'user_review': user_review,
        }

    return render(request, 'moochu/media_detail.html', context)





