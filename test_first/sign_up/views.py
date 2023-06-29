from django.shortcuts import render, redirect
from pymongo import MongoClient

def get_unique_genres():
    # MongoDB 연결
    client = MongoClient('mongodb://localhost:27017/')
    db = client['your_database_name']
    collection = db['your_collection_name']
    
    # 컨텐츠들의 장르 데이터 조회
    genres = collection.distinct('genre')
    
    return genres

def select_genre(request):
    if request.method == 'POST':
        # 폼 제출 처리
        selected_genres = request.POST.getlist('genre')
        # 선택한 장르를 사용자 정보 DB에 저장
        
        # select_content 페이지로 리디렉션
        return redirect('select_content')

    # MongoDB에서 unique한 장르 값들 가져오기
    unique_genres = get_unique_genres()

    return render(request, 'select_genre.html', {'genres': unique_genres})

def select_content(request):
    if request.method == 'POST':
        # 처리할 로직 작성
        # 선택한 컨텐츠를 사용자 정보 DB에 저장
        
        # 다음 페이지로 리디렉션
        return redirect('next_page')

    # 선택된 장르들을 가져오는 로직 작성
    selected_genres = request.session.get('selected_genres', [])
    
    # 선택된 장르와 연관된 컨텐츠를 DB에서 가져오는 로직 작성
    contents = ['컨텐츠1', '컨텐츠2', '컨텐츠3']  # 임시로 가져온 컨텐츠들을 리스트로 설정

    return render(request, 'select_content.html', {'selected_genres': selected_genres, 'contents': contents})
