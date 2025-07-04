from django.shortcuts import render

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

def login(request):
    """Render the login page."""
    return render(request, "login.html", {})

def register(request):
    """Render the register page."""
    return render(request, "register.html", {})