
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Genre

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('common:registration_complete')
    else:
        form = RegistrationForm()
    return render(request, 'common/register.html', {'form': form})

def registration_complete(request):
    return render(request, 'common/registration_complete.html')


## 로그인 함수
def login(request):
    return render(request, 'common/login.html')

## 관심 장르 선택 함수
def genre_selection(request):
    genres = Genre.objects.all()
    return render(request, 'common/genre_selection.html', {'genres': genres})