# Generated by Django 5.1.2 on 2024-12-11 22:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_remove_workout_timestamp_remove_workout_workout_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='exercise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.exercise'),
        ),
    ]
