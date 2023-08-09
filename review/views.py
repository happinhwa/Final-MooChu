from django.shortcuts import render, get_object_or_404, redirect
from moochu.models import Media
from common.models import MovieRating
from . import models, forms
from .models import Review
from bson import ObjectId
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

def convert_to_movie_dict(media_data):
    return {
        'id': str(media_data["_id"]),
        'title': media_data["title_kr"]
    }

# 최신 리뷰 리스트 기본(최신순)
def review(request):
    
    reviews = Review.objects.order_by('-create_date')
    review_all = []

    for review in reviews:
        media_id = review.media_id
        media_data = Media.collection.find_one({'_id': ObjectId(media_id)})
        movie = convert_to_movie_dict(media_data)

        data1 = {'movie':movie, 'review':review }

        review_all.append(data1)
    context = {
        'reviews': review_all,
    }

    return render(request, 'review/review_all.html', context)


def get_movie_data(media_id):
    movie = Media.collection.find_one({"_id": ObjectId(media_id)})
    return movie



# 해당 영화 리뷰 리스트 기본(최신순)
def review_by_id(request, movie_id):
    reviews = Review.objects.filter(media_id=str(movie_id)).order_by('-create_date')
    
    data = convert_to_movie_dict(Media.collection.find_one({"_id": ObjectId(movie_id)}))

    review_all = []
    for review in reviews:
        data1={'review': review, 'movie':data}
        review_all.append(data1)

    context = {
        'review_all': False, 
        'reviews': review_all,
        'movie_id': movie_id,
        }
    
    return render(request, 'review/review_all.html', context)


def review_detail(request, movie_id, review_id):

    review = get_object_or_404(models.Review, pk=review_id)
    voted = review.voter.filter(id=request.user.id).exists()
    is_writer = request.user == review.writer


    data = list(Media.collection.find({"_id": ObjectId(movie_id)}))
    data =[
        {
            'id': str(movie['_id']),
            'titleKr': movie['title_kr'],
        }
        for movie in data
    ]

    context = {
        'movie': data[0],
        'review': review,
        'voted': voted,
        'is_writer': is_writer,
    }

    response = render(request, 'review/review_detail.html', context)


    if not request.COOKIES.get(f'post_{review_id}_viewed'):  # 쿠키 확인
        review.update_counter()  # 조회수 증가
        response.set_cookie(f'post_{review_id}_viewed', 'true')  # 쿠키 설정

    return response



@login_required
def review_upload(request, movie_id):
    if request.method == "POST":
        form = forms.review_form(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.create_date = timezone.now()
            review.writer = request.user
            review.media_id = movie_id
            review.save()
            return redirect('moochu:movie_detail', movie_id=review.media_id)
    else:
        form = forms.review_form()

    data = list(Media.collection.find({"_id": ObjectId(movie_id)}))
    data =[
        {
            'id': str(movie['_id']),
            'titleKr': movie['title_kr'],
        }
        for movie in data
    ]

    context = {
        'form': form,
        'movie': data[0],
    }

    return render(request, 'review/review_upload.html', context)



@login_required
def review_edit(request, movie_id, review_id):
    review = get_object_or_404(models.Review, pk=review_id)
    
    if request.user != review.writer:
        return redirect('moochu:movie_detail', movie_id=review.media_id)

    if request.method == "POST":
        form = forms.review_form(request.POST, instance=review)
        if form.is_valid():
            Review = form.save(commit=False)
            Review.writer = request.user
            Review.modify_date = timezone.now()
            Review.save()
            return redirect('moochu:movie_detail', movie_id=review.media_id)
    else:
        form = forms.review_form(instance=review)
    
    data = list(Media.collection.find({"_id": ObjectId(movie_id)}))
    data =[
        {
            'id': str(movie['_id']),
            'titleKr': movie['title_kr'],
        }
        for movie in data
    ]

    context = {
        'form': form,
        'movie': data[0],
    }
    return render(request, 'review/review_upload.html', context)


@login_required
def review_delete(request, review_id):
    review = get_object_or_404(models.Review, pk=review_id)
    if request.user != review.writer:
        return redirect('moochu:movie_detail', movie_id=review.media_id)

    # 삭제 전 이전 페이지의 URL을 가져옴
    previous_url = request.META.get('HTTP_REFERER')

    review.delete()

    # 이전 페이지로 리다이렉트
    return redirect(previous_url)





################################################################################################################

def ajax_login_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Login required'}, status=401)
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# media_rating 뷰 함수에 적용할 Ajax 인증 데코레이터
@ajax_login_required
def media_rating(request, movie_id):
    user = request.user

    try:
        media_id = ObjectId(movie_id)
    except:
        return JsonResponse({'error': 'Invalid movie ID'}, status=400)
    
    data = list(Media.collection.find({"_id": ObjectId(movie_id)}))
    movie = {
        'id': str(data[0]['_id']),
        'posterImageUrl': data[0]['poster_image_url'],
        'titleKr': data[0]['title_kr'],
        'age': data[0]['rating'],
        'genre': data[0]['genres'],
        'synopsis': data[0]['synopsis'],
        'date': data[0]['released_At'],
    }

    current_rating = None
    try:
        movie_rating = MovieRating.objects.get(user=user, media_id=media_id)
        current_rating = movie_rating.rating
    except MovieRating.DoesNotExist:
        pass

    if request.method == 'POST':
        if 'rating' in request.POST:
            rating = request.POST['rating']

            try:
                movie_rating = MovieRating.objects.get(user=user, media_id=media_id)
                movie_rating.rating = rating
                movie_rating.save()
            except MovieRating.DoesNotExist:
                movie_rating = MovieRating(user=user, media_id=media_id, rating=rating)
                movie_rating.save()

            current_rating = rating

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)

    

    context = {
        'movie': movie,
        'current_rating': current_rating,
    }
    return render(request, 'moochu/media_detail.html', context)






