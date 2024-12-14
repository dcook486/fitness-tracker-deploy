from django.shortcuts import render, redirect
from .models import Workout, Category, Exercise
from .forms import CombinedWorkoutForm, CustomWorkoutForm, ProfileUpdateForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.db.models import Count
from datetime import datetime, timedelta
from django.db.models.functions import TruncDate
from .models import UserTrainer, Trainer
from .forms import UserTrainerForm


@login_required
def workout_list(request):
    """
    View to display all workouts, ordered by date descending.
    Requires user to be logged in.
    """
    workouts = Workout.objects.all().order_by('-date')
    return render(request, 'tracker/workout_list.html', {'workouts': workouts})


# Updated View to handle both standard and custom workouts
@login_required
def add_workout(request):
    if request.method == 'POST':
        if 'standard_workout' in request.POST:
            form = CombinedWorkoutForm(request.POST)
            custom_form = CustomWorkoutForm()
            if form.is_valid():
                workout = form.save(commit=False)
                workout.user = request.user

                exercise_id = request.POST.get('exercise')
                if exercise_id:
                    try:
                        workout.exercise = Exercise.objects.get(id=exercise_id)
                    except Exercise.DoesNotExist:
                        form.add_error('exercise', 'Selected exercise does not exist.')
                        return render(request, 'tracker/add_workout.html', {'form': form, 'custom_form': custom_form})
                workout.save()
                return redirect('workout_list')
        elif 'custom_workout' in request.POST:
            custom_form = CustomWorkoutForm(request.POST)
            form = CombinedWorkoutForm()
            if custom_form.is_valid():
                custom_workout = custom_form.save(commit=False)
                custom_workout.user = request.user

                exercise_id = request.POST.get('exercise')  # Assuming the field is named 'exercise'
                if exercise_id:
                    try:
                        custom_workout.exercise = Exercise.objects.get(id=exercise_id)
                    except Exercise.DoesNotExist:
                        custom_form.add_error('exercise', 'Selected exercise does not exist.')
                        return render(request, 'tracker/add_workout.html', {'form': form, 'custom_form': custom_form})

                custom_workout.save()
                return redirect('workout_list')
        else:
            form = CombinedWorkoutForm()
            custom_form = CustomWorkoutForm()
    else:
        form = CombinedWorkoutForm()
        custom_form = CustomWorkoutForm()

    return render(request, 'tracker/add_workout.html', {'form': form, 'custom_form': custom_form})


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
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)

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

@login_required
def assign_trainer(request):
    form = (request.POST or None)
    if request.method == 'POST':
        form = (request.POST)
        if form.is_valid():
            assign_trainer = form.cleaned_data['trainer']

    return render(request, 'tracker/assign_trainer.html', {'form': form})

def trainer_assigned(request):
    return render(request, 'tracker/trainer_assigned.html')



