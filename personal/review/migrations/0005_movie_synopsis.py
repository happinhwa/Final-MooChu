# Generated by Django 4.1.9 on 2023-07-05 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_remove_movie_average_rating_remove_movie_likes_count_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='synopsis',
            field=models.TextField(default='This is the default synopsis.'),
        ),
    ]
