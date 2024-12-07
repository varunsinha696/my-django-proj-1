from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser  # Ensure CustomUser is your user model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'role', 'password1', 'password2']

class CustomLoginForm(forms.Form):
    username_or_email = forms.CharField(label="Username or Email", max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
