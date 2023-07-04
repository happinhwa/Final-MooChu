from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    nickname = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=1000)
    gender = models.CharField(max_length=15)
    birth = models.DateField()
    fav_genre = models.CharField(max_length=100, null=True)
    created_at = models.DateField(auto_now_add=True)
    temp = models.DecimalField(max_digits=5, decimal_places=2,default=36.5)
    profile_img = models.ImageField(upload_to="profiles/", null=True)
    # visit_count = models.IntegerField(default=0)
    
    
    # delete colume
    first_name = None
    last_name = None
    last_login = None
    date_joined = None
    
    def get_profile_image_url(self):
        if self.profile_img:
            return self.profile_img.url
        else:
            return settings.DEFAULT_PROFILE_IMAGE
        

    def __str__(self):
        return self.username

class follow(models.Model):
    follower = models.IntegerField()
    following = models.IntegerField()

class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    genre = models.CharField(max_length=10, unique=True)  # 테이블 열 이름과 일치하도록 변경
    class Meta:
        db_table = 'genres2'  # 원래 있던 final.genres2를 메타로 설정
    def __str__(self):
        return self.name
    

# class GuestNote(models.Model):
#     main = models.ForeignKey(User, on_delete=models.CASCADE)
#     writer = models.ForeignKey(User, on_delete=models.RESTRICT)
#     created_at = models.DateTimeField(auto_now_add=True)
#     content = models.TextField()

#     def __str__(self):
#         return self.main