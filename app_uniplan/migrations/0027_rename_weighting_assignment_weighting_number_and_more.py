# Generated by Django 4.0.1 on 2022-02-14 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_uniplan', '0026_assignment_due_week_number_assignment_due_week_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignment',
            old_name='weighting',
            new_name='weighting_number',
        ),
        migrations.AddField(
            model_name='assignment',
            name='weighting_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
