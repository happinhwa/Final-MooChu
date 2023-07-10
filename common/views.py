from django.shortcuts import render, redirect
from .forms import RegistrationForm
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
            next_page = request.POST.get('next', 'moochu:mainpage') # 로그인 후에 다시 원래 있던 페이지로 돌아가게 하는 코드 !! 
            return redirect(next_page) # 로그인 후에 다시 원래 있던 페이지로 돌아가게 하는 코드 !! 
        else:
            # 로그인 실패 처리
            return render(request, 'common/login.html', context={'error': '로그인에 실패하였습니다.'})
    else:
        return render(request, 'common/login.html', {'error': ''})


def mypage_home(request):
    return render(request, 'mypage/mypage.html')

def mypage_mylist(request):
    return render(request, 'mypage/mylist.html')

def mypage_reviews(request):
    return render(request, 'mypage/reviews.html')

def mypage_note(request):
    list_=[1,2,3]
    form = {"list_":list_}
    return render(request, 'mypage/note.html', form)


def mypage_edit(requset):
    pass
## 관심 장르 선택 함수
def genre_selection(request):
    genres = Genre.objects.all()
    return render(request, 'common/genre_selection.html', {'genres': genres})
