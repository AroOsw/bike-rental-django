from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.models import auth
from .forms import RegistrationForm, LoginForm



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

def terms(request):
    """Render the terms of service page."""
    return render(request, "terms.html", {})

# def login_user(request):
#     """Render the login page."""
#     if request.method == "POST":
#         form = LoginForm(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                     login(request, user)
#                     messages.info(request, f"Log In successfully")
#                     return redirect("index")
#     else:
#         form = LoginForm()
#     return render(request, "login.html", {"form": form})
#
def logout_view(request):
    """Log out the user and redirect to the index page."""
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("index")
#
# def register(request):
#     """Render the register page."""
#     if request.method == "POST":
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Account created successfully")
#             return redirect("index")
#     else:
#         form = RegistrationForm()
#     return render(request, 'register.html', {"form": form})


