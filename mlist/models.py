from django.db import models
from pymongo import MongoClient


# Create a MongoDB connection
mongodb_connection_uri = 'mongodb://root:root@localhost:27017/?authSource=admin'
mongodb_client = MongoClient(mongodb_connection_uri)

# tmdb data
mongodb_database_name = 'tmdb'
mongodb_database = mongodb_client[mongodb_database_name]
mongodb_collection_name = 't2022'
mongodb_collection = mongodb_database[mongodb_collection_name]

# 다음영화 개봉예정작 리스트
mongodb_database_name1 = 'daum'
mongodb_database1 = mongodb_client[mongodb_database_name1]
mongodb_collection_name1 = 'daumnetflix'
mongodb_collection1 = mongodb_database1[mongodb_collection_name1]

mongodb_database_name2 = 'daum'
mongodb_database2 = mongodb_client[mongodb_database_name2]
mongodb_collection_name2 = 'daumwatcha'
mongodb_collection2 = mongodb_database2[mongodb_collection_name2]

mongodb_database_name3 = 'daum'
mongodb_database3 = mongodb_client[mongodb_database_name3]
mongodb_collection_name3 = 'daumtheater'
mongodb_collection3 = mongodb_database3[mongodb_collection_name3]

class Movie(models.Model):
    title = models.CharField(max_length=255)
    genres = models.CharField(max_length=255)
    poster_path = models.CharField(max_length=255)
    overview = models.TextField()
    release_date = models.DateField()

    class Meta:
        db_table = 'collection'
        app_label = 'mongodb'

    def __str__(self):
        return self.title

class DaumNetflix(models.Model):
    num = models.IntegerField()
    title = models.CharField(max_length=255)
    img_link = models.CharField(max_length=255)

    class Meta:
        db_table = 'daumnetflix'
        app_label = 'mongodb1'

    def __str__(self):
        return self.title

class DaumWatcha(models.Model):
    num = models.IntegerField()
    title = models.CharField(max_length=255)
    img_link = models.CharField(max_length=255)

    class Meta:
        db_table = 'daumwatcha'
        app_label = 'mongodb2'

    def __str__(self):
        return self.title

class DaumTheater(models.Model):
    num = models.IntegerField()
    title = models.CharField(max_length=255)
    img_link = models.CharField(max_length=255)

    class Meta:
        db_table = 'daumtheater'
        app_label = 'mongodb3'

    def __str__(self):
        return self.title




#from django.db import models
#from pymongo import MongoClient


# Create a MongoDB connection
#mongodb_connection_uri = 'mongodb://root:root@localhost:27017/?authSource=admin'

# tmdb data
#mongodb_client = MongoClient(mongodb_connection_uri)
#mongodb_database_name = 'tmdb'
#mongodb_database = mongodb_client[mongodb_database_name]
#mongodb_collection_name = 't2022'
#mongodb_collection = mongodb_database[mongodb_collection_name]

## Create a MongoDB connection
#mongodb_connection_uri = 'mongodb://root:root@localhost:27017/?authSource=admin'
#mongodb_client = MongoClient(mongodb_connection_uri)
#
## 몽고db에서 tmdb 컬렉션들만 가져오기
#mongodb_database_name = 'tmdb'
#mongodb_database = mongodb_client[mongodb_database_name]
#
## Get a list of all collections in the database
#collections_list = mongodb_database.list_collection_names()
#
## Loop through each collection and perform your desired operation
#for collection_name in collections_list:
#    collection = mongodb_database[collection_name]
#    # Perform your operations using the collection variable
#
#
## 다음영화 개봉예정작 리스트
#mongodb_database_name1 = 'daum'
#mongodb_client1 = MongoClient(mongodb_connection_uri)
#mongodb_database1 = mongodb_client1[mongodb_database_name1]
#mongodb_collection_name1 = 'daumnetflix'
#mongodb_collection1 = mongodb_database1[mongodb_collection_name1]
#
#mongodb_database_name2 = 'daum'
#mongodb_client2 = MongoClient(mongodb_connection_uri)
#mongodb_database2 = mongodb_client2[mongodb_database_name2]
#mongodb_collection_name2 = 'daumwatcha'
#mongodb_collection2 = mongodb_database2[mongodb_collection_name2]
#
#mongodb_database_name3 = 'daum'
#mongodb_client3 = MongoClient(mongodb_connection_uri)
#mongodb_database3 = mongodb_client3[mongodb_database_name3]
#mongodb_collection_name3 = 'daumtheateer'
#mongodb_collection3 = mongodb_database3[mongodb_collection_name3]
#
#class Movie(models.Model):
#    # Define your model fields here
#    # ...
#
#    class Meta:
#        db_table = 'collection'
#        app_label = 'mongodb'
#
#    def __str__(self):
#        return self.title
#
#
##class Movie(models.Model):
##    # Define your model fields here
##    # ...
##
##    class Meta:
##        db_table = 't2022'
##        app_label = 'mongodb'
##
##    def __str__(self):
##        return self.title
##
#
#class Movie1(models.Model):
#    # Define your model fields here
#    # ...
#
#    class Meta:
#        db_table = 'daumnetflix'
#        app_label = 'mongodb1'
#
#    def __str__(self):
#        return self.title
#
#
#class Movie2(models.Model):
#    # Define your model fields here
#    # ...
#
#    class Meta:
#        db_table = 'daumwatcha'
#        app_label = 'mongodb2'
#
#    def __str__(self):
#        return self.title
#
#
#class Movie3(models.Model):
#    # Define your model fields here
#    # ...
#
#    class Meta:
#        db_table = 'daumtheater'
#        app_label = 'mongodb3'
#
#    def __str__(self):
#        return self.title