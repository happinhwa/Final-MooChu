# Generated by Django 4.2.3 on 2023-07-19 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='cast',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='director',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='genre',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='release_date',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='synopsis',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='title',
        ),
        migrations.AlterField(
            model_name='movie',
            name='id',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
        migrations.AlterModelTable(
            name='movie',
            table=None,
        ),
    ]
