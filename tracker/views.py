from django.shortcuts import render, redirect
from .models import Workout
from .forms import WorkoutForm, ProfileUpdateForm, CustomUserCreationForm  # Import ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ExerciseSelectionForm


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
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workout_list')
    else:
        form = WorkoutForm()
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
    form = ExerciseSelectionForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Process the selected exercise (e.g., add to user's workout)
        selected_exercise = form.cleaned_data['exercise']
        # Add code here to save the selected exercise to the user's profile/workout
    return render(request, 'tracker/select_exercise.html', {'form': form})
def workout_list(request):
    workouts = Workout.objects.all()
    form = ExerciseSelectionForm(request.POST or None)
    if form.is_valid():
        # Process the selected exercise
        selected_exercise = form.cleaned_data['exercise']
        # Handle the selected exercise if necessary

    return render(request, 'tracker/workout_list.html', {'workouts': workouts, 'form': form})