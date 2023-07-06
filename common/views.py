from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm,GuestNoteForm,ProfileUpdateForm
from . import models
## 회원가입 
from django.contrib.auth import authenticate, login
from .models import Genre

## 회원가입 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('common:register_complete')
    else:
        form = RegistrationForm()
    return render(request, 'common/register.html', {'form': form})

def register_complete(request):
    return render(request, 'common/register_complete.html')

## 로그인 함수
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('moochu:mainpage')
        else:
            # 로그인 실패 처리
            return render(request, 'common/login.html', context={'error': '로그인에 실패하였습니다.'})

    else:
        return render(request, 'common/login.html', {'error': ''})

def mypage_home(request, nickname):
    writer_id = request.user.id
    master = get_object_or_404(models.User, nickname=nickname)
    writer = get_object_or_404(models.User, id=writer_id)
    following = models.follow.objects.filter(follower=master.id)
    follower = models.follow.objects.filter(following=master.id)
    allow = models.follow.objects.filter(follower=writer, following=master).exists()

    follower_count = follower.count()
    if follower_count == 0:
        follower_count = 0

    following_count = following.count()
    if following_count == 0:
        following_count =0


    form = {"master": master,
            "writer":writer,
            "follow":follow,
            "follower_count": follower_count,
            "following_count": following_count,
            "allow":allow,
            "follower": follower,
            "following": following,}
    return render(request, 'mypage/mypage.html', form)

def mypage_mylist(request, nickname):
    writer_id = request.user.id
    master = get_object_or_404(models.User, nickname=nickname)
    writer = get_object_or_404(models.User, id=writer_id)
    following = models.follow.objects.filter(follower=master.id)
    follower = models.follow.objects.filter(following=master.id)
    allow = models.follow.objects.filter(follower=writer, following=master).exists()

    follower_count = follower.count()
    if follower_count == 0:
        follower_count = 0

    following_count = following.count()
    if following_count == 0:
        following_count =0


    form = {"master": master,
            "writer":writer,
            "follow":follow,
            "follower_count": follower_count,
            "following_count": following_count,
            "allow":allow,
            "follower": follower,
            "following": following,}
    return render(request, 'mypage/mylist.html', form)

def mypage_reviews(request, nickname):
    writer_id = request.user.id
    master = get_object_or_404(models.User, nickname=nickname)
    writer = get_object_or_404(models.User, id=writer_id)
    following = models.follow.objects.filter(follower=master.id)
    follower = models.follow.objects.filter(following=master.id)
    allow = models.follow.objects.filter(follower=writer, following=master).exists()
    reviews = models.review.objects.filter(user_id=master.id)

    follower_count = follower.count()
    if follower_count == 0:
        follower_count = 0

    following_count = following.count()
    if following_count == 0:
        following_count =0


    form = {"master": master,
            "writer":writer,
            "follow":follow,
            "follower_count": follower_count,
            "following_count": following_count,
            "allow":allow,
            "follower": follower,
            "following": following,
            "reviews":reviews,}
    
    return render(request, 'mypage/reviews.html', form)

def mypage_note(request, nickname):
    if request.method == 'POST':
        form = GuestNoteForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            master = get_object_or_404(models.User, nickname=nickname)
            writer_id = request.user.id
            master_id = models.User.objects.get(id=master.id)
            writer_user = models.User.objects.get(id=writer_id)

            models.GuestNote.objects.create(
                content=content,
                main=master_id,
                writer=writer_user
            )
            return redirect('common:note' ,master.nickname)
    
    writer_id = request.user.id
    master = get_object_or_404(models.User, nickname=nickname)
    writer = get_object_or_404(models.User, id=writer_id)
    following = models.follow.objects.filter(follower=master.id)
    follower = models.follow.objects.filter(following=master.id)
    allow = models.follow.objects.filter(follower=writer, following=master).exists()
    note = models.GuestNote.objects.filter(main=master.id).order_by('-created_at')

    follower_count = follower.count()
    if follower_count == 0:
        follower_count = 0

    following_count = following.count()
    if following_count == 0:
        following_count =0


    form = {"master": master,
            "writer":writer,
            "follow":follow,
            "follower_count": follower_count,
            "following_count": following_count,
            "allow":allow,
            "follower": follower,
            "following": following,
            "note": note,}
    
    return render(request, 'mypage/note.html', form)


def mypage_edit(request, nickname):
    writer_id = request.user.id
    master = get_object_or_404(models.User, nickname=nickname)
    writer = get_object_or_404(models.User, id=writer_id)
    following = models.follow.objects.filter(follower=master.id)
    follower = models.follow.objects.filter(following=master.id)
    allow=models.follow.objects.filter(follower=writer, following=master).exists()
    
    follower_count = follower.count()
    if follower_count == 0:
        follower_count = 0

    following_count = following.count()
    if following_count == 0:
        following_count =0
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            nickname = form.cleaned_data['nickname']
            return redirect('common:mypage', nickname)
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    
    context = {"master": master,
            "writer":writer,
            "follow":follow,
            "follower_count": follower_count,
            "following_count": following_count,
            "allow":allow,
            'form': form}
    
    return render(request, 'mypage/edit.html', context)


## 관심 장르 선택 함수
def genre_selection(request):
    genres = Genre.objects.all()
    return render(request, 'common/genre_selection.html', {'genres': genres})


## 방명록 삭제
def delete(request, guestnote_id):
    note_item = models.GuestNote.objects.get(id=guestnote_id)
    note_item.delete()
    note = models.GuestNote.objects.all()
    user= models.User.objects.all()
    list_=[1,2,3]
    form = {"list_":list_,
            "note": note,
            "user": user}
    return render(request, 'mypage/note.html', form)


## 사용자의 리뷰 전체 list
def reviews_total(request):
    pass


## 사용자의 평점 전체 list
def votes(request):
    pass


def follow(request):
    if request.method == 'POST':
        master_id = request.POST.get('master_id')
        master = models.User.objects.get(id=master_id)
        # follower 테이블에 입력하는 로직
        models.follow.objects.create(follower=request.user, following= master)
        
        
        return redirect('common:mypage', master.nickname )
    
    
def follow_de(request):
    if request.method == 'POST':
        master_id = request.POST.get('master_id')
        master = models.User.objects.get(id=master_id)
        # follower 테이블에 입력하는 로직
        models.follow.objects.get(follower=request.user, following= master).delete()
        
        
        return redirect('common:mypage', master.nickname )