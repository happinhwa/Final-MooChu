from django.shortcuts import render, redirect

# Create your views here.
from rest_framework.views import APIView  
from rest_framework.response import Response  
from rest_framework import status  
from elasticsearch import Elasticsearch  
  
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
   
def search(request):
    return render(request, 'search/home.html')
