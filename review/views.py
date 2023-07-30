from django.shortcuts import render, get_object_or_404, redirect
from moochu.models import Media
from . import models, forms
from bson import ObjectId
from django.utils import timezone
from django.contrib.auth.decorators import login_required



# 리뷰 리스트 기본(최신순)
def review(request):
    review_list = models.Review.objects.order_by('-create_date')
    
    context = {'review_list': review_list}
    
    return render(request, 'review/review_list.html', context)


def review_detail(request, movie_id, review_id):
    ## TV 또는 MOVIE에 맞게 media 리스트 저장
    data = list(Media.collection.find({"_id": ObjectId(movie_id)}))
    ## 필요한 데이터 형식으로 변형
    data =[
        {
            'id': str(movie['_id']),
            'posterImageUrl': movie['poster_image_url'],
            'titleKr': movie['title_kr'],
        }
        for movie in data
    ]

        # data에서 정보를 가져와서 새로운 Review 객체 생성 및 저장
    movie_info = data[0]
    review = models.Review.objects.create(
        posterImageUrl=movie_info['posterImageUrl'],
        titleKr=movie_info['titleKr'],
        # 필요한 다른 필드들을 여기에 추가합니다.
    )
    context = {
            'movie': data[0],
            'review': review, 
            'voted': voted, 
            'is_writer': is_writer
        }
    

    review = get_object_or_404(models.Review, pk=review_id)
    voted = review.voter.filter(id=request.user.id).exists()
    is_writer = request.user == review.writer
    
    response = render(request, 'review/review_detail.html', context)
    
    if not request.COOKIES.get(f'review_{review_id}_viewed'):  # 쿠키 확인
        review.update_counter()  # 조회수 증가
        response.set_cookie(f'review_{review_id}_viewed', 'true')  # 쿠키 설정
    
    return response

@login_required
def review_upload(request, movie_id):
    if request.method == "POST":
        form = forms.review_form(request.POST)
        if form.is_valid():
            models.Review = form.save(commit=False)
            models.Review.create_date = timezone.now()
            models.Review.writer = request.user
            models.Review.save()
            return redirect('review:review')
    else:
        form = forms.review_form()


    data = list(Media.collection.find({"_id": ObjectId(movie_id)}))
    ## 필요한 데이터 형식으로 변형
    data =[
        {
            'id': str(movie['_id']),
        }
        for movie in data
    ]

    context = {
        'movie': data[0],
        'form': form
    }
    

    return render(request, 'review/review_upload.html', context)