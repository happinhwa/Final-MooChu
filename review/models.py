from django.db import models
from django.utils import timezone
from common.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    release_date = models.DateField()
    director = models.CharField(max_length=255)
    cast = models.TextField()
    synopsis = models.TextField(default="작성된 영화 줄거리가 없습니다.")
    def __str__(self):
        return str(self.title)
    class Meta:
        db_table = 'movie'
        app_label = 'review'

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_writer')
    review = models.TextField(default="작성된 리뷰가 없습니다.")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
    liker = models.ManyToManyField(User, related_name='review_liker')
    vote = models.FloatField(null=True)
  
    def __str__(self):
        return str(self.review)
        
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    comment_txt = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return str(self.comment_txt)

    
