from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import Movie, Review, Comments
from django.urls import reverse
from .forms import ReviewForm, CommentsForm
from django.contrib.auth.decorators import login_required




# 임시 영화 데이터

def movie_list(request):
    movies = Movie.objects.all()
    context= {'movies': movies}
    return render(request, 'review/movie_list.html',context)

def movie_detail(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    return render(request, 'review/movie_detail.html', {'movie': movie})



# 구현해야 하는 리뷰 기능들

def main_review_list(request):
    user = request.user
    reviews = Review.objects.filter(user=user).order_by('-timestamp')
    context = {'reviews': reviews}
    return render(request, 'review/main_review_list.html', context)

def main_review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'review/main_review_detail.html', {'review': review})


def write_review(request, movie_id):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie_id = movie_id
            review.save()
            return HttpResponseRedirect(reverse('review:main_review_list'))
    else:
        form = ReviewForm()
        movie = Movie.objects.get(pk=movie_id)
        context = {'form': form, 'movie': movie}
         
    return render(request, 'review/write_review.html', context)

"""
def review_comment(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect('review:main_review_detail', review_id=review_id)
    else:
        form = CommentForm()
    return render(request, 'review/review_comment.html', {'form': form, 'review': review})
"""

def review_comment(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    all_comments = review.comment_set.all()
    
    if request.method == 'POST':
        form = CommentsForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
        else:
            pass
    else:
        form = CommentsForm()
    return render(request, 'review/review_comment.html', {'form': form, 'review': review, 'all_comments': all_comments})

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