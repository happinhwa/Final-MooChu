from django.shortcuts import render, redirect, get_object_or_404
from urllib3 import HTTPResponse
from .forms import RegistrationForm
## 회원가입 
from django.contrib.auth import authenticate, login
from .models import Genre
from rest_framework.decorators import api_view

# from rest_framework.renderers import JSONRenderer
# from rest_framework.views import APIView
# from rest_framework.response import Response


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
            return redirect('moochu:main')
        else:
            # 로그인 실패 처리
            return render(request, 'common/login.html', context={'error': '로그인에 실패하였습니다.'})

    else:
        return render(request, 'common/login.html', {'error': ''})

## 관심 장르 선택 함수
def genre_selection(request):
    genres = Genre.objects.all()
    return render(request, 'common/genre_selection.html', {'genres': genres})

