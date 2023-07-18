from pathlib import Path
import os
from django.conf import settings
import logging
from django.utils import timezone
import logstash

class UserRequestsFilter(logging.Filter): #로그 필터
    def filter(self, record):
        request = getattr(record, "request", None)
        if request is not None:
            user_id = getattr(request.user, "id", "anonymous")
            logging_start_time = getattr(request, "_logging_start_time", timezone.now())
            request_time = timezone.localtime(logging_start_time).strftime('%Y-%m-%d %H:%M:%S')
            extra_user_id = getattr(record, "user_id", None) # user_id를 extra에서 가져옵니다.
            extra_post_id = getattr(record, "post_id", None) # post_id를 extra에서 가져옵니다.

            record.user_id = user_id
            record.extra_user_id = extra_user_id # extra_user_id 추가
            record.extra_post_id = extra_post_id # extra_post_id 추가
            record.request_time = request_time
            record.path = request.path
        return True


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'common.User'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-z+i-5d9*d+s!vp_a+6#aj(hvwaciv0_+!2a*(0a!bqia$^c)i&"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "common",
    "board",
    "moochu",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "mypage"
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'), 
            os.path.join(BASE_DIR, 'templates', 'accounts')
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
AUTH_USER_MODEL = 'common.User'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME':'final',
        'USER':'encore',
        'PASSWORD':'tlrdl13!#',
        'HOST':'127.0.0.1',
        'PORT':'4000'
    },
    # 'test_mongo': {
    #     'ENGINE': 'djongo',
    #     'NAME': 'final_db',
    #     'CLIENT': {
    #         'host': 'localhost',
    #         'port': '4001',
    #         'username': 'root',
    #         'password': 'root',
    #         'authSource': 'admin',
    #         'authMechanism': 'SCRAM-SHA-1'
    #     }
    # }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'user_requests': {
            '()': 'config.settings.UserRequestsFilter',
        },
    },
    'formatters': {
        'detailed': {
            'format': '{levelname} {asctime} User[{user_id}] postID[{extra_post_id}] Path[{path}] {message}',
            'style': '{',
        },
        'movie_verbose': {
            'format': '{levelname} {asctime} User[{user_id}] {message}',
            'style': '{',
        },
    },
        'handlers': {
            'boardlogfile': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'board.log',
                'maxBytes': 1024*1024*5,
                'backupCount': 10,
                'filters': ['user_requests'],
                'formatter': 'detailed',
            },
            'commonlogfile': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'common.log',
                'maxBytes': 1024*1024*5,
                'backupCount': 10,
                'filters': ['user_requests'],
                'formatter': 'detailed',
            },
            'moochulogfile': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'moochu.log',
                'maxBytes': 1024*1024*5,
                'backupCount': 10,
                'filters': ['user_requests'],
                'formatter': 'detailed',
            },
            'mypagelogfile': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'mypage.log',
                'maxBytes': 1024*1024*5,
                'backupCount': 10,
                'filters': ['user_requests'],
                'formatter': 'detailed',
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': 'renderMV.log',  
                'formatter': 'movie_verbose',
            },
    },
            'loggers': {
                'board': {
                    'handlers': ['boardlogfile'],
                    'level': 'DEBUG',
                },
                'common': {
                    'handlers': ['commonlogfile'],
                    'level': 'INFO',
                },
                'moochu': {
                    'handlers': ['moochulogfile'],
                    'level': 'INFO',
                },
                'mypage': {
                    'handlers': ['mypagelogfile'],
                    'level': 'INFO',
                },
                'common': {  # 앱 이름으로 변경하세요.
                    'handlers': ['file'],
                    'level': 'DEBUG',
                    'propagate': False,
                },

        },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# 장고디비에 이미지 파일올리기

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
# ACCOUNT_EMAIL_REQUIRED = True
# # ACCOUNT_AUTHENTICATION_METHOD = "email"
# ACCOUNT_EMAIL_CONFIRMATION_EMAIL_TEMPLATE = 'account/email_confirmation.html'

# # Email sending
# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGIN_REDIRECT_URL = "/moochu"
LOGOUT_REDIRECT_URL = "/moochu"
ACCOUNT_LOGOUT_ON_GET = True
# EMAIL_HOST = 'smtp.gmail.com'
# # 메일을 호스트하는 서버
# EMAIL_PORT = '587'
# # gmail과의 통신하는 포트
# EMAIL_HOST_USER = '----'
# # 발신할 이메일
# EMAIL_HOST_PASSWORD = '-----'
# # 발신할 메일의 비밀번호
# EMAIL_USE_TLS = True
# # TLS 보안 방법
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# # 사이트와 관련한 자동응답을 받을 이메일 주소,'webmaster@localhost'


# 기본 프로필 이미지 경로 설정
DEFAULT_PROFILE_IMAGE = 'media/profiles/chuchu.png'  # 기본 이미지 파일의 경로
