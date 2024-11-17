from django.shortcuts import render, redirect
from .models import Workout, Category
from .forms import CombinedWorkoutForm, CustomWorkoutForm, ProfileUpdateForm, CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Exercise

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
    """
    Handles adding a standard workout and custom workout.
    """
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    if request.method == 'POST':
        # Check if adding a standard workout
        if 'standard_workout' in request.POST:
            standard_form = CombinedWorkoutForm(request.POST)
            if standard_form.is_valid():
                standard_form.save()
                return redirect('workout_list')
        # Check if adding a custom workout
        elif 'custom_workout' in request.POST:
            custom_form = CustomWorkoutForm(request.POST)
            if custom_form.is_valid():
                custom_form.save()
                return redirect('workout_list')
    else:
        standard_form = CombinedWorkoutForm()
        custom_form = CustomWorkoutForm()

    return render(request, 'tracker/add_workout.html', {
        'standard_form': standard_form,
        'custom_form': custom_form,
    })

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

def home(request):
    return render(request, 'tracker/home.html')
