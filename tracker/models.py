
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='exercises')
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

class Workout(models.Model):
    WORKOUT_TYPES = [
        ('cardio', 'Cardio'),
        ('upper_body', 'Upper Body'),
        ('lower_body', 'Lower Body'),
        ('weight_lifting', 'Weight Lifting'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES)
    duration = models.IntegerField(null=True, blank=True)
    sets = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    workout_date = models.DateField("Workout Date(mm/dd/year)", auto_now_add=False, auto_now=False, blank=True, null=True)
    timestamp = models.DateField(auto_now_add=True, auto_now=False, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.exercise.name} - {self.get_workout_type_display()} on {self.date.strftime('%Y-%m-%d')}"


