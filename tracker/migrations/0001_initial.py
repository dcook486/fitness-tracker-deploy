# Generated by Django 5.1.2 on 2024-10-14 22:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_type', models.CharField(choices=[('cardio', 'Cardio'), ('upper_body', 'Upper Body'), ('lower_body', 'Lower Body'), ('weight_lifting', 'Weight Lifting')], max_length=20)),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('sets', models.IntegerField(blank=True, null=True)),
                ('reps', models.IntegerField(blank=True, null=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]