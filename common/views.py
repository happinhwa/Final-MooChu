<<<<<<< HEAD
from django.shortcuts import render, redirect, get_object_or_404
from urllib3 import HTTPResponse
=======
from django.shortcuts import render, redirect
>>>>>>> 3032e914fe1914a652206ebf0f7c3eb61199ceca
from .forms import RegistrationForm
## 회원가입 
from django.contrib.auth import authenticate, login
from .models import Genre
from rest_framework.decorators import api_view

<<<<<<< HEAD
# from rest_framework.renderers import JSONRenderer
# from rest_framework.views import APIView
# from rest_framework.response import Response


## 회원가입 
=======
>>>>>>> 3032e914fe1914a652206ebf0f7c3eb61199ceca
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
<<<<<<< HEAD
            form.save()
            return redirect('common:register_complete')
=======
            user = form.save()
            
>>>>>>> 3032e914fe1914a652206ebf0f7c3eb61199ceca
    else:
        form = RegistrationForm()
    return render(request, 'common/register.html', {'form': form})

<<<<<<< HEAD
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
<<<<<<< HEAD
            return redirect('moochu:main')
=======
            next_page = request.POST.get('next', 'moochu:mainpage') # 로그인 후에 다시 원래 있던 페이지로 돌아가게 하는 코드 !! 
            return redirect(next_page) # 로그인 후에 다시 원래 있던 페이지로 돌아가게 하는 코드 !! 
>>>>>>> 0546c39ed2ec3f8bccdb5b89a32ab92669e8d244
        else:
            # 로그인 실패 처리
            return render(request, 'common/login.html', context={'error': '로그인에 실패하였습니다.'})
    else:
        return render(request, 'common/login.html', {'error': ''})

## 관심 장르 선택 함수
def genre_selection(request):
    genres = Genre.objects.all()
    return render(request, 'common/genre_selection.html', {'genres': genres})

=======
def registration_complete(request):
    return render(request, 'common/registration_complete.html')



## 로그인 함수
def login(request):
    return render(request, 'common/login.html')
>>>>>>> 3032e914fe1914a652206ebf0f7c3eb61199ceca
