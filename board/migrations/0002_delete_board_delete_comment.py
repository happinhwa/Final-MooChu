# Generated by Django 4.2 on 2023-06-28 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("board", "0001_initial"),
    ]

    operations = [
        migrations.DeleteModel(
            name="board",
        ),
        migrations.DeleteModel(
            name="comment",
        ),
    ]
