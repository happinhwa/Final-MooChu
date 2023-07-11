
# Generated by Django 4.2.2 on 2023-07-06 00:59


from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="board",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=30)),
                ("content", models.CharField(max_length=1000)),
                ("edit_date", models.DateField(auto_now_add=True)),
                ("created_at", models.DateField(auto_now_add=True)),
                (
                    "writer",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="board_writer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.CharField(max_length=1000)),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                ("like_count", models.IntegerField()),
                (
                    "board_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="board.board"
                    ),
                ),
                (
                    "writer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_writer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
