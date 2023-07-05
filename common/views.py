from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm
from . import models
from .forms import GuestNoteForm
## 회원가입 
from .models import Genre

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('common:registration_complete')
    else:
        form = RegistrationForm()
    return render(request, 'common/register.html', {'form': form})

def registration_complete(request):
    return render(request, 'common/registration_complete.html')


## 로그인 함수
def login(request):
    return render(request, 'common/login.html')

def mypage_home(request):
    ## user_id=request.user.id
    ## user = get_object_or_404(models.User, id=user_id)    
    user = models.User.objects.filter(id="1")
    form = {"user": user}
    return render(request, 'mypage/mypage.html', form)

def mypage_mylist(request):
    user= models.User.objects.all()
    form = {"user": user}
    return render(request, 'mypage/mylist.html', form)

def mypage_reviews(request):
    user= models.User.objects.all()
    form = {"user": user}
    return render(request, 'mypage/reviews.html', form)

def mypage_note(request):
    if request.method == 'POST':
        form = GuestNoteForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            main_id ="1"
            writer_id="2"
            main_user = models.User.objects.get(id=main_id)
            writer_user = models.User.objects.get(id=writer_id)

            models.GuestNote.objects.create(
                content=content,
                main=main_user,
                writer=writer_user
            )
            return redirect('common:note')
    note = models.GuestNote.objects.all()
    user= models.User.objects.all()
    form = {"note": note,
            "user": user}
    return render(request, 'mypage/note.html', form)


def mypage_edit(requset):
    pass


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


