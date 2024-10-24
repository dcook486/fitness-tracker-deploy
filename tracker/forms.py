from django import forms
from .models import Workout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['workout_type', 'duration', 'sets', 'reps']

class CustomUserCreationForm(UserCreationForm):  # Add this new form
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', ]  # Specify the fields you want to allow editing

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # You can customize fields here if necessary
        self.fields['username'].required = True  # Ensure the username is required