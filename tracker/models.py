from django.db import models


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

    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES)
    duration = models.IntegerField(null=True, blank=True)  # for cardio workouts
    sets = models.IntegerField(null=True, blank=True)  # for strength workouts
    reps = models.IntegerField(null=True, blank=True)  # for strength workouts
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_workout_type_display()} on {self.date.strftime('%Y-%m-%d')}"
