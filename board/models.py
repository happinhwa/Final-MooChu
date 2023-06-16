from django.db import models

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
