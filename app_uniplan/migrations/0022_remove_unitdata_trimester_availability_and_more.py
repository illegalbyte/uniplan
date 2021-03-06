# Generated by Django 4.0.1 on 2022-02-12 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_uniplan', '0021_remove_majorsequence_units_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='unitdata',
            name='trimester_availability',
        ),
        migrations.AddField(
            model_name='unitdata',
            name='trimester_availability_json',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='UnitAvailability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('burwood', models.BooleanField(default=False)),
                ('cloud', models.BooleanField(default=False)),
                ('geelong', models.BooleanField(default=False)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_uniplan.semester')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_uniplan.unit')),
            ],
        ),
    ]
