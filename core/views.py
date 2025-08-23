from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from core.models import BikeModel, BikeInstance, Reservation
from django.contrib.auth.models import auth
from .forms import RegistrationForm, LoginForm


# Create your views here.


def index(request):
    """Render the index page."""

    return render(request, "index.html", {})

def bikes(request):
    """Render the bikes page."""
    all_bikes = BikeInstance.objects.all()
    print(all_bikes)
    return render(request, "bikes.html", {"all_bikes": all_bikes})

def routes(request):
    """Render the routes page."""
    return render(request, "routes.html", {})

def reservations(request):
    """Render the reservations page."""
    return render(request, "reservations.html", {})

def contact(request):
    """Render the contact page."""
    return render(request, "contact.html", {})

def terms(request):
    """Render the terms of service page."""
    return render(request, "terms.html", {})

@login_required
def profile(request):
    """Render the user profile page."""
    if request.user.is_authenticated:
        user = request.user
        return render(request, "profile.html", {"user": user})
    else:
        messages.error(request, "You need to be logged in to view your profile.")
        return redirect("index")

def logout_view(request):
    """Log out the user and redirect to the index page."""
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("index")


