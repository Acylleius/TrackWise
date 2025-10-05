# accounts/views.py
#trisha backend
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages



def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another.")
            return redirect("accounts:register")

        # Check for short password
        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return redirect("accounts:register")

        # Check for mismatched passwords
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:register")

        # If all good, create user
        user = User.objects.create_user(username=username, password=password1)
        user.save()
        messages.success(request, "Account created successfully! You can now log in.")
        return redirect("accounts:login")

    return render(request, 'accounts/register.html')

# --- Login View ---
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if username exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Username does not exist.")
            return redirect("accounts:login")

        # Authenticate user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, f"Welcome back, {username}!")
            return redirect("dashboard:dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("accounts:login")

    return render(request, "accounts/login.html")





 