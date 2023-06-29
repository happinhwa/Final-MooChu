from django.db import models

# Create your models here.

class Users(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=10)
    nickname = models.CharField(max_length=15)
    email = models.EmailField(max_length=20)
    password = models.CharField(max_length=30)
    gender = models.IntegerField()
    birth = models.DateField()
    fav_genre = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)# 가입일시

class Mypage(models.Model):
    temp = models.DecimalField(max_digits=65, decimal_places=2)
    visit_count = models.IntegerField()
    profile_img = models.ImageField(upload_to="profiles/", null=True)

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