from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import  Review, Comments
from django.db.models import Count
from django.urls import reverse
from .forms import ReviewForm, CommentsForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import OTT_detail




# 임시 영화 데이터

def movie_list(request):
    movies = OTT_detail.objects.all()
    context= {'movies': movies}
    return render(request, 'review/movie_list.html',context)



def movie_detail(request, id):
    movie = OTT_detail.get_movie_by_id(id)
    if movie:
        # Add review functionality
        if request.method == "POST":
            form = ReviewForm(request.POST)
            if form.is_valid():
                review = form.save(commit=False)
                review.user = request.user
                # Set the necessary movie details in the review
                review.movie_id = id
                review.save()
                return redirect('mlist:movie_detail', id=id)
        else:
            form = ReviewForm()

        return render(request, 'mlist/movie_detail.html', {'movie': movie, 'form': form})
    else:
        return redirect('movie_not_found')  



# 구현해야 하는 리뷰 기능들

def main_review_list(request, movie_id):
    movie = Movie.objects.get(pk=movie_id)
    reviews = Review.objects.filter(movie_id=movie_id)
    order = request.GET.get("order")
    print(order)
    
    if order == "newest":
        reviews = reviews.order_by('-timestamp')
    elif order == "likes":
        reviews = reviews.annotate(num_likes=Count('liker')).order_by('-num_likes')
    elif order == "rating":
        reviews = reviews.order_by("-vote")
    elif order == "comments":
        reviews = reviews.annotate(num_comments=Count('comments')).order_by('-num_comments')
    else:
        reviews = reviews.order_by('-timestamp')

    
    counts = reviews.annotate(num_comments=Count('review'), num_likes=Count('liker'))
    context = {'movie':movie, 'reviews': reviews, 'counts':counts}

    return render(request, 'review/main_review_list.html', context)


def main_review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'review/main_review_detail.html', {'review': review})

from django.shortcuts import get_object_or_404


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import ReviewForm
from common.models import Review, OTT_detail
from django.http import HttpResponse

@login_required
def write_review(request, movie_id):
    # Prepopulate the movie_title field with the title of the movie
    movie = OTT_detail.get_movie_by_id(movie_id)
    movie_title = movie['title_kr']

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            user_id = request.user.id

            # Fetch the movie based on the movie_title from MongoDB
            try:
                movie = OTT_detail['all'].find_one({'title_kr': movie_title})
                print("MongoDB Query Result:", movie)
            except Exception as e:
                print("Error:", e)
                return HttpResponse("Movie not found!")

            # Save the review to the database
            review = Review(user_id=user_id, movie_title=movie['title'], create_date=timezone.now())
            review.save()
            print('title_kr')
            return redirect('mlist:movie_detail', id=movie_id)
    else:
        form = ReviewForm(initial={'movie_title': movie_title})

    context = {'form': form, 'title_kr': movie_title}
    return render(request, 'review/write_review.html', context)










def write_comment(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    user = request.user
    comment_txt = request.POST.get('content')
    form = CommentsForm(request.POST)  # Comment_form에서 CommentsForm으로 변경합니다.
    if form.is_valid():
        comment = form.save(commit=False)
        comment.review = review
        comment.writer = user
        comment.save()
        return redirect('review:main_review_detail', review_id=review.id)
    else:
        # 유효하지 않은 폼인 경우 다시 폼을 생성해서 사용자에게 보여줌
        form = CommentsForm()

    return render(request, 'review/write_comment.html', {'form': form, 'review': review})


@login_required
def review_update(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.user:
        messages.error(request, '수정권한이 없습니다')
        return redirect('review:main_review_detail', review_id=review.id)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(commit=False)
            review.review = updated_review.review  # 리뷰 내용 업데이트
            review.updated_at = timezone.now()  # 수정일시 저장
            review.save()
            return redirect('review:main_review_detail', review_id=review.id)
    else:
        form = ReviewForm(instance=review)
    
    # 이전에 작성한 리뷰 작성 페이지로 돌아가기 위해 movie_id를 가져옴
    movie_id = review.movie.pk
    context = {'form': form, 'movie_id': movie_id, 'review_id': review_id}
    return render(request, 'review/review_update.html', context)

@login_required
def comment_update(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    if request.user != comment.user:
        messages.error(request,'수정권한이 없습니다')
        return redirect('review:main_review_detail', comment_id=comment.id)
    
    if request.method == "POST":
        form = CommentsForm(request.POST, instance=comment)
        if form.is_valid():
            updated_comment = form.save(commit=False)
            comment.comment_txt = updated_comment.comment_txt
            comment.updated_at = timezone.now()
            comment.save()
            return redirect('review:main_review_detail', review_id=comment.review.pk)
    else:
        form = CommentsForm(instance=comment)
    
    context = {'form': form, 'comment_id': comment_id}
    return render(request, 'review/comment_update.html', context)

@login_required
def review_delete(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user != review.user:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('review:main_review_detail', review_id=review.id)

    review.delete()
    return redirect('review:main_review_list', movie_id=review.movie.pk)

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    if request.user != comment.user:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('review:main_review_detail', comment_id=comment.id)

    comment.delete()
    return redirect('review:main_review_detail', review_id=comment.review.pk)


# main_review_list로 보낼거
@login_required
def review_liker1(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.user:
        messages.error(request, '본인이 작성한 글에 좋아요를 누를 수 없습니다')
    else:
        if request.user in review.liker.all():
            review.liker.remove(request.user)  # 좋아요 취소
        else:
            review.liker.add(request.user)  # 좋아요 추가
    return redirect('review:main_review_list', movie_id=review.movie.id)
# main_review_detail로 보낼거
@login_required
def review_liker2(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.user:
        messages.error(request, '본인이 작성한 글에 좋아요를 누를 수 없습니다')
    else:
        if request.user in review.liker.all():
            review.liker.remove(request.user)  # 좋아요 취소
        else:
            review.liker.add(request.user)  # 좋아요 추가
    return redirect('review:main_review_detail', review_id=review.id)

def newest_review_list(request):
    reviews = Review.objects.all().order_by('-timestamp')
    context= {'reviews': reviews}
    return render(request, 'review/newest_review_list.html',context)