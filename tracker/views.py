from django.shortcuts import render, redirect
from .models import Workout
from .forms import CombinedWorkoutForm, ProfileUpdateForm, CustomUserCreationForm  # Import ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.template.loader import render_to_string
from .models import Exercise
from django.shortcuts import render

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

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    if request.method == 'POST':
        form = CombinedWorkoutForm(request.POST)
        if form.is_valid():
            form.save()
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

def workout_list(request):
    workouts = Workout.objects.all()
    form = CombinedWorkoutForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():

        pass

    return render(request, 'tracker/workout_list.html', {'workouts': workouts, 'form': form})

def load_exercises(request):
    category_id = request.GET.get('category_id')
    exercises = Exercise.objects.filter(category_id=category_id)
    exercise_list = [{"id": exercise.id, "name": exercise.name} for exercise in exercises]
    return JsonResponse(exercise_list, safe=False)