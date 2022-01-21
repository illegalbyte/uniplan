# Generated by Django 4.0.1 on 2022-01-21 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app_uniplan', '0009_alter_semester_end_date_alter_semester_start_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='total_marks_available',
            field=models.IntegerField(blank=True, help_text='The total marks available for the assignment', null=True),
        ),
        migrations.AlterField(
            model_name='unit',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]