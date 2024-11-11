from django.shortcuts import render, redirect
from .models import Workout
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

def load_exercises(request):
    category_id = request.GET.get('category_id')
    exercises = Exercise.objects.filter(category_id=category_id)
    exercise_list = [{"id": exercise.id, "name": exercise.name} for exercise in exercises]
    return JsonResponse(exercise_list, safe=False)

#Show exercise history
@login_required
def exercise_history(request):
    # Get filter parameters from request
    exercise_filter = request.GET.get('exercise')
    category_filter = request.GET.get('category')
    date_filter = request.GET.get('date_range')

    # Start with all workouts
    workouts = Workout.objects.all()

    # Apply filters if they exist
    if exercise_filter:
        workouts = workouts.filter(exercise__name=exercise_filter)
    if category_filter:
        workouts = workouts.filter(category__name=category_filter)

    # Date range filtering
    if date_filter:
        today = datetime.now().date()
        if date_filter == 'week':
            start_date = today - timedelta(days=7)
            workouts = workouts.filter(date__gte=start_date)
        elif date_filter == 'month':
            start_date = today - timedelta(days=30)
            workouts = workouts.filter(date__gte=start_date)
        elif date_filter == 'year':
            start_date = today - timedelta(days=365)
            workouts = workouts.filter(date__gte=start_date)

    # Order by date descending
    workouts = workouts.order_by('-date')

    # Get exercise categories and names for filter dropdowns
    categories = workouts.values_list('category__name', flat=True).distinct()
    exercises = workouts.values_list('exercise__name', flat=True).distinct()

    # Get some basic stats
    total_workouts = workouts.count()
    most_common_exercise = workouts.values('exercise__name').annotate(
        count=Count('exercise__name')).order_by('-count').first()

    context = {
        'workouts': workouts,
        'categories': categories,
        'exercises': exercises,
        'total_workouts': total_workouts,
        'most_common_exercise': most_common_exercise['exercise__name'] if most_common_exercise else None,
        'selected_exercise': exercise_filter,
        'selected_category': category_filter,
        'selected_date_range': date_filter,
    }

    return render(request, 'tracker/exercise_history.html', context)