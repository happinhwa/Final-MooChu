from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import render, redirect
from .models import Genre
import random
from pymongo import MongoClient
from .forms import RegistrationForm

from django.utils.encoding import force_bytes

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_str as force_text


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # 이메일 인증 링크 생성
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain
            link = f'http://{domain}/activate/{uid}/{token}/'
            
            # 이메일 전송
            mail_subject = '회원가입 확인 이메일'
            message = render_to_string('common/activation_email.html', {
                'user': user,
                'link': link,
            })
            email = EmailMessage(mail_subject, message, to=[user.email])
            email.send()
            
            return redirect('registration_complete')
    else:
        form = RegistrationForm()
    return render(request, 'common/register.html', {'form': form})

def registration_complete(request):
    return render(request, 'common/registration_complete.html')

def genre_selection(request):
    genres = Genre.objects.all()
    return render(request, 'common/genre_selection.html', {'genres': genres})



def get_mongo_connection():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['test']
    collection = db['movie']
    return collection

def get_recommended_movies(user_genres):
    collection = get_mongo_connection()
    movies = list(collection.find({"gen": {"$in": user_genres}})) # 회원가입시에 받은 장르들
    random.shuffle(movies)
    return movies[:5]

def firstmovie(request):
    # 사용자의 선택에 따른 장르를 얻어옵니다.
    # 세션을 사용하는 경우, 아래와 같이 세션에서 장르를 가져옵니다.
    user_genres = request.session.get('selected_genres', [])
    recommended_movies = get_recommended_movies(user_genres)
    return render(request, 'common/firstmovie_page.html', {'recommended_movies': recommended_movies})


