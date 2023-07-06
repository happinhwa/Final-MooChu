from django.db import migrations, models
import django.db.models.deletion


def handle_null_values(apps, schema_editor):
    SelectedGenre = apps.get_model('common', 'SelectedGenre')
    for obj in SelectedGenre.objects.filter(user__isnull=True):
        obj.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20230706_1041.py'),  # Replace '<timestamp>' with the actual timestamp in the previous migration filename
    ]

    operations = [
        migrations.RunPython(handle_null_values),
        migrations.AlterField(
            model_name='selectedgenre',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.User'),
        ),
    ]

