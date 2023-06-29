from djongo import models

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    class Meta:
        db_table = 'my_model_collection'  # MongoDB 컬렉션 이름 설정
