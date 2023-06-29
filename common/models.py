from django.db import models
from django.contrib.auth.models import AbstractUser

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
    
    def __str__(self):
        return self.email

class follow(models.Model):
    follower = models.IntegerField()
    following = models.IntegerField()