# Generated by Django 4.0.1 on 2022-02-13 22:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_uniplan', '0023_semester_active_semester_semester_past_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='semester',
            old_name='past',
            new_name='is_past',
        ),
    ]
