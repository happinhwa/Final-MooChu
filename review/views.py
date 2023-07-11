from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Movie, Review, Comments
from django.db.models import Count
from django.urls import reverse
from .forms import ReviewForm, CommentsForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages




# 임시 영화 데이터

def movie_list(request):
    movies = Movie.objects.all()
    context= {'movies': movies}
    return render(request, 'review/movie_list.html',context)

def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    return render(request, 'review/movie_detail.html', {'movie': movie})



# 구현해야 하는 리뷰 기능들

def main_review_list(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    reviews = Review.objects.filter(movie_id=movie_id).order_by('-timestamp')
    counts =  reviews.annotate(num_comments=Count('review'), num_likes=Count('liker'))
    context = {'movie':movie, 'reviews': reviews, 'counts':counts}
    return render(request, 'review/main_review_list.html', context)

def main_review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'review/main_review_detail.html', {'review': review})


def write_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = movie
            review.save()
            return redirect('review:main_review_list', movie_id=movie.id)
    else:   
        form = ReviewForm()
    context = {'form': form, 'movie': movie}

    return render(request, 'review/write_review.html', context)


def write_comment(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    user = request.user
    comment_txt = request.POST.get('content')
    print(f'comment_txt: {comment_txt}')  # 로그 출력
    comment = Comments(review=review, comment_txt=comment_txt, user=user, created_at=timezone.now())
    comment.save()
    return redirect('review:main_review_detail', review_id=review.id)

"""
@login_required
def delete_comment(request, pk):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comments, pk=comment_id)
        if request.user == comment.user:
            comment.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failed', 'message': '댓글을 삭제할 권한이 없습니다.'})
    else:
        return JsonResponse({'status': 'failed', 'message': '잘못된 요청입니다.'})
"""