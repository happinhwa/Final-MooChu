# Generated by Django 4.2 on 2023-07-05 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0004_merge_20230705_1007"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="comment",
            field=models.CharField(default="한줄소개가 아직 없습니다.", max_length=100),
        ),
    ]
