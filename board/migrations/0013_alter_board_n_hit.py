
from django.db import migrations

def update_n_hit(apps, schema_editor):
    Board = apps.get_model('board', 'board')
    Board.objects.filter(n_hit__isnull=True).update(n_hit=0)

class Migration(migrations.Migration):

    dependencies = [
        ('board', '0012_alter_board_n_hit'),
    ]

    operations = [
        migrations.RunPython(update_n_hit),
    ]

