from django.db import migrations


def create_sample_worker(apps, schema_editor):
    Worker = apps.get_model('workers', 'Worker')
    if not Worker.objects.exists():
        Worker.objects.create(name='Іван Петренко', salary=10000, notes='Приклад працівника')


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_sample_worker),
    ]
