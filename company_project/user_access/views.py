from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomLoginForm

def custom_login(request):
    """
    Handles user login.
    Authenticates based on email or username and password.
    """
    if request.method == 'POST':
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']
            
            # Check if user exists with email or username
            user = authenticate(request, username=username_or_email, password=password) or \
                   authenticate(request, email=username_or_email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('product-list')  # Redirect to product list or desired view
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = CustomLoginForm()
    
    return render(request, 'user_access/login.html', {'form': form})


def register(request):
    """
    Handles user registration.
    Assigns default role as 'Viewer' if not explicitly set.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Assign default role as 'Viewer'
            if not user.role:
                user.role = 'viewer'
                user.save()
            
            # Log the user in after successful registration
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect('product_list')  # Redirect to product list or desired view
        else:
            messages.error(request, "Error during registration. Please correct the form.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'user_access/register.html', {'form': form})
