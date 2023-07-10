# Generated by Django 4.2.2 on 2023-07-03 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Genre",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("genre", models.CharField(max_length=10, unique=True)),
            ],
            options={
                "db_table": "genres2",
            },
        ),
    ]