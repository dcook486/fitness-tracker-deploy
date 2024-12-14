# models.py
from django.db import models
from django.contrib.auth.models import User

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

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, null=True, blank=True)
    workout_type = models.CharField(max_length=20, choices=WORKOUT_TYPES)
    duration = models.IntegerField(null=True, blank=True)
    sets = models.IntegerField(null=True, blank=True)
    reps = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        exercise_name = self.exercise.name if self.exercise else "No Exercise"
        return f"{self.exercise.name} - {self.get_workout_type_display()} on {self.date.strftime('%Y-%m-%d')}"

#trainer model
class Trainer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='trainer')

    def __str__(self):
        return self.user.username

#user trainer
class UserTrainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} is assigned to {self.trainer.user.username}'
