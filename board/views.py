from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from . import models, forms
from django.contrib import messages
from django.http import HttpResponse


############## Post 관련 ##############

def moobo(request):
    post_list = models.board.objects.order_by('-create_date')
    return render(request, 'board/moobo.html', {'post_list': post_list})



def detail(request, post_id):
    post = get_object_or_404(models.board, pk=post_id)
    voted = post.voter.filter(id=request.user.id).exists()
    is_writer = request.user == post.writer
    
    response = render(request, 'board/post_detail.html', {'post': post, 'voted': voted, 'is_writer': is_writer})
    
    if not request.COOKIES.get(f'post_{post_id}_viewed'):  # 쿠키 확인
        post.update_counter()  # 조회수 증가
        response.set_cookie(f'post_{post_id}_viewed', 'true')  # 쿠키 설정
    
    return response


@login_required
def post(request):
    if request.method == "POST":
        form = forms.post_form(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.create_date = timezone.now()
            board.writer = request.user
            board.save()
            return redirect('board:moobo')
    else:
        form = forms.post_form()

    context = {'form': form}
    return render(request, 'board/post.html', context)




############## Comment 관련 ##############

def comment(request, post_id):
    post = get_object_or_404(models.board, pk=post_id)
    post.comment_set.create(content=request.POST.get('content'), create_date=timezone.now())
    return redirect('board:detail', post_id = post.id)





@login_required
def comment_create(request, post_id):
    """
    pybo 질문댓글등록
    """
    post = get_object_or_404(models.board, pk=post_id)
    if request.method == "POST":
        form = forms.comment_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.writer = request.user
            comment.create_date = timezone.now()
            comment.board = post
            comment.save()
            return redirect('{}#comment_{}'.format(
                resolve_url('board:post_detail', post_id=comment.board.id), comment.id))
    # elif request.method == "DELETE":
    #     ## 삭제하는 로직 

    # elif request.method == "PUT":
    #     ## 수정하는 로직 
    else:
        form = forms.comment_form()
    context = {'form': form}
    return render(request, 'board/comment_create.html', context)



############## 추천 관련 ##############

@login_required
def vote_post(request, post_id):
    """
    pybo 질문추천등록
    """
    post = get_object_or_404(models.board, pk=post_id)
    if request.user == post.writer:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    elif post.voter.filter(id=request.user.id).exists():
        messages.error(request, '이미 추천했습니다')
    else:
        post.voter.add(request.user)
    
    return redirect('board:post_detail', post_id=post.id)


@login_required
def vote_comment(request, comment_id):
    """
    pybo 답글추천등록
    """
    comment = get_object_or_404(comment, pk=comment_id)
    if request.user == comment.writer:
        messages.error(request, '본인이 작성한 글은 추천할수 없습니다')
    elif comment.voter.filter(id=request.user.id).exits():
        messages.error(request, '이미 추천했습니다')
    else:
        comment.voter.add(request.user)
    return redirect('board:post_detail', post_id=comment.board.id)
