from django.db import models
from django.conf import settings
from django.utils import timezone



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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    content = models.TextField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_date = models.DateField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    

    def __str__(self):
        return self.content

    class Meta:
        db_table = 'review'
        app_label = 'review'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.content

    class Meta:
        db_table = 'comment'
        app_label = 'review'