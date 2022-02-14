# Generated by Django 4.0.1 on 2022-02-14 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_uniplan', '0025_rename_active_semester_semester_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='due_week_number',
            field=models.IntegerField(blank=True, help_text='The week of the semester the assignment is due', null=True),
        ),
        migrations.AddField(
            model_name='assignment',
            name='due_week_text',
            field=models.CharField(blank=True, help_text='The week of the semester the assignment is due', max_length=30, null=True),
        ),
    ]
