from django.db import models
from django.utils import timezone
from common.models import User



class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    release_date = models.DateField()
    director = models.CharField(max_length=255)
    cast = models.TextField()
    synopsis = models.TextField(default="This is the default synopsis.")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'movie'
        app_label = 'review'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    review = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'review'
        app_label = 'review'


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    re_comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.content

    class Meta:
        db_table = 'comment'
        app_label = 'review'