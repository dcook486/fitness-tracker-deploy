# Generated by Django 5.1.2 on 2024-11-15 20:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name="Exercise",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="exercises",
                        to="tracker.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Workout",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "workout_type",
                    models.CharField(
                        choices=[
                            ("cardio", "Cardio"),
                            ("upper_body", "Upper Body"),
                            ("lower_body", "Lower Body"),
                            ("weight_lifting", "Weight Lifting"),
                        ],
                        max_length=20,
                    ),
                ),
                ("duration", models.IntegerField(blank=True, null=True)),
                ("sets", models.IntegerField(blank=True, null=True)),
                ("reps", models.IntegerField(blank=True, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "exercise",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tracker.exercise",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-date"],},
        ),
    ]
