from django.shortcuts import render, redirect
from .models import Workout, Category
from .forms import CombinedWorkoutForm, ProfileUpdateForm, CustomUserCreationForm  # Import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Exercise
from django.shortcuts import render
from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate


@login_required
def workout_list(request):
    """
     View to display all workouts, ordered by date descending.
     Requires user to be logged in.
     """
    workouts = Workout.objects.all().order_by('-date')
    return render(request, 'tracker/workout_list.html', {'workouts': workouts})

# View to add a new workout
@login_required
def add_workout(request):
    if request.method == 'POST':
        form = CombinedWorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)  # Don't save to DB yet
            workout.user = request.user  # Set the user
            workout.save()  # Now save to DB
            return redirect('workout_list')
    else:
        form = CombinedWorkoutForm()
    return render(request, 'tracker/add_workout.html', {'form': form})

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})

# New profile view to update user information
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)  # Use ProfileUpdateForm instead of UserChangeForm
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to the profile page after saving
    else:
        form = ProfileUpdateForm(instance=request.user)  # Use ProfileUpdateForm instead of UserChangeForm

    return render(request, 'tracker/profile.html', {'form': form})

def select_exercise(request):
    form = (request.POST or None)
    if request.method == 'POST':
        form = (request.POST)
        if form.is_valid():
            selected_exercise = form.cleaned_data['exercise']

    return render(request, 'tracker/workout_list.html', {'form': form})

def load_exercises(request):
    category_id = request.GET.get('category_id')
    exercises = Exercise.objects.filter(category_id=category_id)
    exercise_list = [{"id": exercise.id, "name": exercise.name} for exercise in exercises]
    return JsonResponse(exercise_list, safe=False)


@login_required
def exercise_history(request):
    # Filter workouts for the current user and order by date
    workouts = Workout.objects.filter(user=request.user).order_by('-date')

    context = {
        'workouts': workouts,
    }

    return render(request, 'tracker/exercise_history.html', context)