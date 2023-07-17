from django.shortcuts import render, redirect, get_object_or_404
from urllib3 import HTTPResponse
from .forms import RegistrationForm
## 회원가입 
from django.contrib.auth import authenticate, login
from .models import Genre, User
from rest_framework.decorators import api_view
# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode



## 회원가입 
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            current_site = get_current_site(request) 
            message = render_to_string('common/register_activation.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_title = "계정 활성화 확인 이메일"
            mail_to = request.POST["email"]
            email = EmailMessage(mail_title, message, to=[mail_to])
            email.send()
            address = "http://www." + mail_to.split('@')[1]
            form = { "user": user,
                    "address": address }
            return render(request, 'common/register_complete.html', form)
    else:
        form = RegistrationForm()
    return render(request, 'common/register.html', {'form': form})

def register_complete(request):
    user=request.user
    address = "http://www." + user.email.split('@')[1]
    form = {"address":address}
    return render(request, 'common/register_complete.html', form)

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

## 관심 장르 선택 함수
def genre_selection(request):
    genres = Genre.objects.all()
    return render(request, 'common/genre_selection.html', {'genres': genres})


# 계정 활성화 함수(토큰을 통해 인증)
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExsit):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect("common:authentication")
    
def authentication(request):
    return render(request, 'common/Authentication_complete.html')