from django.db import models
from django.utils import timezone
from common.models import User, MovieRating

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
    vote = models.FloatField(null=True, blank=True)  # 평점을 저장할 필드
    rating = models.ForeignKey(MovieRating, on_delete=models.SET_NULL, null=True, blank=True)  # MovieRating의 id 값을 받는 필드
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)

    def __str__(self):
        return str(self.review)

    def save(self, *args, **kwargs):
        try:
            rating = MovieRating.objects.get(user=self.user, movie_title=self.movie.title).rating
            self.vote = rating
        except MovieRating.DoesNotExist:
            self.vote = None  # 평점이 없을 경우 None으로 설정
        super().save(*args, **kwargs)
        
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    comment_txt = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True, auto_now=True)
  
    def __str__(self):
        return str(self.comment_txt)

    
