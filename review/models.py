# models.py
from django import forms
from django.utils import timezone
from django.db import models
from common.models import User, MovieRating
from django.conf import settings
from mlist.models import OTT_detail



#class Movie(models.Model):
#    id = models.CharField(max_length=255, primary_key=True)
#    title = models.CharField(max_length=255)
#
#    def __str__(self):
#        return str(self.title)
#
#    class Meta:
#        db_table = 'movie'
#        app_label = 'review'



class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_written', default=None)
    content = models.TextField()
    create_date = models.DateField(auto_now_add=True)
    modify_date = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    voter = models.ManyToManyField(User, related_name='voter_reviews')
    updated_at = models.DateTimeField(null=True, blank=True)
    n_hit = models.PositiveIntegerField(default=0)
    movie_id = models.TextField()

    def update_counter(self):
        self.n_hit += 1
        self.save()




class Comments(models.Model):
    writer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments_written')
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
    comment_txt = models.TextField(null=True)
    timestamp = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.writer.username + "님의 댓글"

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.updated_at = timezone.now()
        super().save(*args, **kwargs)
