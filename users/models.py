from django.db import models

# Create your models here.

class users(models.Model):
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


class comment(models.Model):
    board_id = models.IntegerField()
    content = models.CharField(max_length=1000)
    create_date = models.DateTimeField(auto_now_add=True)
    like_count = models.IntegerField()
    writer = models.CharField(max_length=500)

class board(models.Model):
    title = models.CharField(max_length=30)
    content = models.CharField(max_length=1000)
    edit_date = models.DateField(auto_now_add=True)
    created_at = models.DateField(auto_now_add=True)
