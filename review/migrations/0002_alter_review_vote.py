# Generated by Django 4.2.3 on 2023-07-11 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='vote',
            field=models.FloatField(null=True),
        ),
    ]
