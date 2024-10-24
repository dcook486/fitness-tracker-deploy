from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic import RedirectView
from . import views


urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False), name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='tracker/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('add/', views.add_workout, name='add_workout'),
    path('workouts/', views.workout_list, name='workout_list'),
    path('profile/', views.profile, name='profile'),
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="tracker/password_reset.html"),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="tracker/password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="tracker/password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="tracker/password_reset_done.html"),
         name='reset_reset_complete'),
]