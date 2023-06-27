from django.db import models

# Create your models here.

class Users(models.Model):
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=30)
    gender = models.IntegerField()
    birth = models.DateField()
    fav_genre = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)

class Mypage(models.Model):
    temp = models.DecimalField(max_digits=100, decimal_places=2)
    visit_count = models.IntegerField()
    profile_img = models.ImageField(upload_to="profiles/", null=True)

class follow(models.Model):
    follower = models.IntegerField()
    following = models.IntegerField()