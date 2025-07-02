from django.shortcuts import render

# Create your views here.


def index(request):
    """Render the index page."""
    return render(request, "index.html", {})

def bikes(request):
    """Render the bikes page."""
    return render(request, "bikes.html", {})