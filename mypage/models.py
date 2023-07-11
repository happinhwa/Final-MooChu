from django.db import models
from common.models import User

# Create your models here.
class follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')



class GuestBook(models.Model):
    main = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main')
    writer = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='writer')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return str(self.main)
    
class mylist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mylist_user_id')
    media_title = models.CharField(max_length=20)
    media_poster = models.ImageField(upload_to="posters/", null=True)


    def __str__(self):
        return str(self.user_id)


class review(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_user_id')
    movie_title = models.CharField(max_length=100)
    content = models.CharField(max_length=500)
    
    def __str__(self):
        return str(self.user_id)

class votes(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='vote_user_id')
    movie_title = models.CharField(max_length=20)
    score = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return str(self.user_id)

