from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from elasticsearch import Elasticsearch  
from moochu.models import Media
from collections import OrderedDict
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

  
def trans(hits):
    hits_list=[]
    for hit in hits:
        hits_list.append(hit['_source'])

    return hits_list[:10]


class SearchView(APIView):
    def get(self, request):
        es = Elasticsearch(hosts=["34.64.147.118:9200"])

        search_word = request.GET.get('search')

        if not search_word:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'search word param is missing'})

        docs = es.search(
            index='movies',
            body={
                "query": {
                    "multi_match": {
                        "query": search_word,
                        "fields": ["title_kr","title_En", "genres"]                    
                    }
                }
            }
        )

        # data_list = trans(docs['hits']['hits'])
        data_list = docs['hits']['hits']
        if data_list:
            return Response({'data': data_list})
            # return render(request, 'search/result.html',{'data': data_list})
        else:
            return Response({'data': data_list})
            # return render(request, 'search/result.html')

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

def search(request):
    pipeline = [
            {"$match": {"media_type": "MOVIE","indexRating.score": {"$gte": 95}}},
            {"$sample": {"size": 1000}}  # 임시로 충분히 큰 숫자를 지정해 무작위 순서로 문서들을 반환받는다.
        ]

    movies = Media.collection.aggregate(pipeline)

    # 중복제거
    unique_movies = OrderedDict()
    for movie in movies:
        if movie['title_kr'] not in unique_movies:
            unique_movies[movie['title_kr']] = movie
    data = list(unique_movies.values())[:20]

    page_obj= data_change(request,data)

    context = {
        'data': page_obj,
    }

    return render(request, 'search/home.html', context)
