from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages



# Create your views here.


def index(request):
    """Render the index page."""
    return render(request, "index.html", {})

def bikes(request):
    """Render the bikes page."""
    return render(request, "bikes.html", {})

def routes(request):
    """Render the routes page."""
    return render(request, "routes.html", {})

def reservations(request):
    """Render the reservations page."""
    return render(request, "reservations.html", {})

def contact(request):
    """Render the contact page."""
    return render(request, "contact.html", {})

def login_user(request):
    """Render the login page."""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username, password)  # Debug
        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.info(request, f"Log In successfully")
            login(request, user)
            return redirect("index")  # Przekierowanie po zalogowaniu
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
    return render(request, "login.html", {})

def logout_user(request):
    """Log out the user and redirect to the index page."""
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("index")

def register(request):
    """Render the register page."""
    return render(request, "register.html", {})



