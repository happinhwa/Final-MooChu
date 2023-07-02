
from django.shortcuts import render, redirect
from .forms import RegistrationForm

## 회원가입 
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