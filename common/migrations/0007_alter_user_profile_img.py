# Generated by Django 4.2 on 2023-07-05 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0006_alter_user_profile_img"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="profile_img",
            field=models.ImageField(default="/static/abc.jpg", upload_to="profiles/"),
        ),
    ]