# Generated by Django 4.0.1 on 2022-02-13 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_uniplan', '0024_rename_past_semester_is_past'),
    ]

    operations = [
        migrations.RenameField(
            model_name='semester',
            old_name='active_semester',
            new_name='is_active',
        ),
    ]
