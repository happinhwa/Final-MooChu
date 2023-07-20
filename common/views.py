from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm,GenreSelectForm
from .models import Genre,SelectedGenre,MovieRating,User
from pymongo import MongoClient
from bson.objectid import ObjectId
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from urllib3 import HTTPResponse
## 회원가입 
from django.contrib.auth import authenticate, login
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

GENRE_CHOICES = {
    1: '액션',
    2: '코미디',
    3:'드라마',
    4:'공포',
    5:'스릴러',
    6:'로맨스',
    7:'서부',
    8:'전쟁',
    9:'판타지',
    10:'미스터리'

    # 나머지 번호와 장르를 추가하세요.
}

def get_genre_name(genre_id):
    return GENRE_CHOICES.get(genre_id, 'Unknown')

@login_required
def movie_selection(request):
    if request.method == 'POST':
        message = ""
        user = request.user

        db = get_mongo_db()  # 기존에 사용된 MongoDB 접속 함수를 가져옵니다.

        movies = db['movie'].find({})  # MongoDB에 저장된 모든 영화 정보를 가져옵니다.

        for movie in movies:
            movie_id = str(movie['_id'])
            movie_title_key = f"movie_title_{movie_id}"
            rating_key = f"rating_{movie_id}"
            if movie_title_key in request.POST and rating_key in request.POST:
                movie_title = request.POST[movie_title_key]
                rating = request.POST[rating_key]

                try:
                    movie_rating = MovieRating(user=user, movie_title=movie_title, rating=rating)
                    movie_rating.save()
                    message = "영화 평점 저장이 완료되었습니다."
                except ValidationError:
                    message = "영화 평점 저장에 실패했습니다. 다시 시도해 주세요."
            else:
                message = "영화 평점 정보가 누락되었습니다."

        return render(request, 'common/register_complete.html', {'message': message})
    else:
        client = MongoClient('mongodb://localhost:27017/')
        db = client['test']
        collection = db['movie']
        #select_genres = SelectedGenre.objects.values_list('genre', flat=True)
        select_genres = SelectedGenre.objects.filter(user=request.user).values_list('genre', flat=True)  # 가져온 필드를 사용하여 장르를 선택
        select_genre_names = [get_genre_name(int(g)) for g in select_genres]  # 선택된 장르 번호를 이름으로 매핑

        # 수정할 부분: 선택한 장르와 관련된 영화
        movies = collection.find({"gen": {"$elemMatch": {"$in": select_genre_names}}})  
        print(select_genres)

        #movies = collection.find({"gen": {"$elemMatch": {"$in": list(select_genres)}}})
        print(movies)

        movie_str = []
        for movie in movies:
            movie['m_id'] = str(movie['_id'])
            movie_str.append(movie)

        return render(request, 'common/movie_selection.html', {'movies': movie_str})
    
def get_mongo_db():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['test']
    return db


def genre_selection(request):
    if request.method == 'POST':
        form = GenreSelectForm(request.POST)
        if form.is_valid():
            user = request.user
            selected_genres = form.cleaned_data.get('selected_genres')

            for genre in selected_genres: 
                # 이미 Genre 객체이므로 genre_id를 사용할 필요가 없습니다.
                selected_genre = SelectedGenre(user=user, genre=genre) 
                selected_genre.save()

            return redirect('common:movie_selection')
    else:
        form = GenreSelectForm()
        genres = Genre.objects.all()

        return render(request, 'common/genre_selection.html', {'form': form, 'genres': genres})


@login_required
def save_genre(request):
    all_genres = get_all_genres()

    if request.method == 'POST':
      form = GenreSelectForm(request.POST, genre_choices=all_genres)
      if form.is_valid():
            selected_genres = form.cleaned_data['selected_genres']
            for genre_choice_id in selected_genres:
                choice_text = form.fields['selected_genres'].choices_dict.get(genre_choice_id)
                selected_genre = SelectedGenre(genre=choice_text)
                selected_genre.save()
                print(f'장르 저장 완료: {choice_text}')  
            return render(request, 'common/genre_selection.html')
    else:
        form = GenreSelectForm(genre_choices=all_genres)

    return render(request, 'common/genre_selection.html', {'form': form})


# 계정 활성화 함수(토큰을 통해 인증)
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)
        return redirect("common:authentication")
    
def authentication(request):
    return render(request, 'common/Authentication_complete.html')