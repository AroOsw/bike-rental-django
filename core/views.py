from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from core.models import BikeModel, BikeInstance, Reservation
from .forms import BookingForm
from django.http import JsonResponse


def index(request):
    """Render the index page."""
    return render(request, "index.html", {})

def bikes(request, slug):
    """Render the bikes page."""
    if slug == "all":
        all_bikes = BikeModel.objects.prefetch_related("instances")
        return render(request, "bikes.html", {
            "all_bikes": all_bikes,

        })
    bike_type = BikeModel.objects.filter(type=slug).all()
    print(bike_type)
    return render(request, "bikes.html", {
        "all_bikes": bike_type,
    })


def bike_details(request, slug):
    """Render the individual bike page."""
    bike_model = get_object_or_404(BikeModel.objects.prefetch_related("instances"), slug=slug)

    pricing_data = {
        "day_1_2": bike_model.calculate_rental_price(1),
        "day_3_6": bike_model.calculate_rental_price(3),
        "day_7_13": bike_model.calculate_rental_price(7),
        "day_14": bike_model.calculate_rental_price(14),
    }

    if request.method == "POST":
        booking_form = BookingForm(request.POST, bike_model=bike_model)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.start_time = booking_form.cleaned_data["start_time"]
            booking.end_time = booking_form.cleaned_data["end_time"]
            booking.user = request.user
            booking.bike_model = bike_model
            booking.save()
            messages.success(request, "Your booking has been submitted successfully!")
            return redirect("bike_details", slug=slug)
        else:
            messages.error(request, "Something went wrong. Please check the form for errors.")
            # print(booking_form.errors.as_text())
    else:
        booking_form = BookingForm(bike_model=bike_model)

    return render(request, "bike-details.html", {
        "bike_model": bike_model,
        "pricing_data": pricing_data,
        "form": booking_form,
    })

def routes(request):
    """Render the routes page."""
    return render(request, "routes.html", {})

def get_bike_reservations(request, bike_instance_id):
    """API endpoint to get reservations for a specific bike instance."""
    try:
        bike_instance = BikeInstance.objects.get(id=bike_instance_id)
        reservations = Reservation.objects.filter(bike_instance=bike_instance).values("start_time", "end_time")
        reservation_list = [
            {
                "start_time": res["start_time"].isoformat(),
                "end_time": res["end_time"].isoformat()
            } for res in reservations
        ]
        return JsonResponse({"reservations": reservation_list})
    except BikeInstance.DoesNotExist:
        return JsonResponse({"error": "Bike instance not found."}, status=404)

def reservations(request):
    """Render the reservations page."""
    if request.user.is_authenticated:
        user_reservations = Reservation.objects.filter(user=request.user).order_by("-created_at")
        return render(request, "reservations.html", {
            "reservations": user_reservations,
        })
    return render(request, "reservations.html", {
    })

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
