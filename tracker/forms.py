from django import forms
from .models import Workout, Category, Exercise
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CombinedWorkoutForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.none(), required=True, label="Select Exercise")

    class Meta:
        model = Workout
        fields = ['exercise', 'workout_type']  # Only include the required fields
        widgets = {
            'exercise': forms.Select(attrs={'class': 'form-control'}),
            'workout_type': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['exercise'].queryset = Exercise.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        else:
            self.fields['exercise'].queryset = Exercise.objects.all()


class CustomWorkoutForm(forms.ModelForm):
    exercise = forms.ModelChoiceField(queryset=Exercise.objects.all(), required=True, label="Select Exercise")

    class Meta:
        model = Workout
        fields = ['exercise', 'workout_type', 'duration', 'sets', 'reps']
        widgets = {
            'exercise': forms.Select(attrs={'class': 'form-control'}),
            'workout_type': forms.Select(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control'}),
            'sets': forms.NumberInput(attrs={'class': 'form-control'}),
            'reps': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']  # Specify the fields you want to allow editing

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        # You can customize fields here if necessary
        self.fields['username'].required = True  # Ensure the username is required


