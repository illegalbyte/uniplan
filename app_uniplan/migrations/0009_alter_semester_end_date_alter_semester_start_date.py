# Generated by Django 4.0.1 on 2022-01-21 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_uniplan', '0008_alter_student_profile_course_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='semester',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='semester',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
