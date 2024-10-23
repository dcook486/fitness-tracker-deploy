from django.shortcuts import render, redirect
from .models import Workout
from .forms import WorkoutForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import render, redirect
from .models import Workout
from .forms import WorkoutForm, ProfileUpdateForm  # Import ProfileUpdateForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required


@login_required
def workout_list(request):
    workouts = Workout.objects.all()
    return render(request, 'tracker/workout_list.html', {'workouts': workouts})

# View to display all workouts
def workout_list(request):
    workouts = Workout.objects.all().order_by('-date')
    return render(request, 'tracker/workout_list.html', {'workouts': workouts})

# View to add a new workout
def add_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('workout_list')
    else:
        form = WorkoutForm()
    return render(request, 'tracker/add_workout.html', {'form': form})

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
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

