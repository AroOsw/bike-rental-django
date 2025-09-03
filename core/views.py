from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from core.models import BikeModel, BikeInstance, Reservation
from .forms import BookingForm, EditBookingForm
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


def calculate_price_ajax(request, bike_model_id):
    """Simply endpoint to calculate price."""
    try:
        days = int(request.GET.get('days', 1))
        bike_model = BikeModel.objects.get(id=bike_model_id)
        price_per_day_after_discount = bike_model.calculate_rental_price(days)
        total_price = price_per_day_after_discount * days


        return JsonResponse({
            'total_price': float(total_price),
            'price_per_day': float(price_per_day_after_discount),
            'days': days
        })
    except BikeModel.DoesNotExist:
        return JsonResponse({'error': 'Bike not found'}, status=404)


def get_bike_reservations(request, bike_instance_id):
    """API endpoint to get reservations for a specific bike instance."""
    try:
        bike_instance = BikeInstance.objects.get(id=bike_instance_id)
        all_reservations = Reservation.objects.filter(bike_instance=bike_instance).values("start_time", "end_time")
        reservation_list = [
            {
                "start_time": res["start_time"].isoformat(),
                "end_time": res["end_time"].isoformat()
            } for res in all_reservations
        ]
        return JsonResponse({"reservations": reservation_list})
    except BikeInstance.DoesNotExist:
        return JsonResponse({"error": "Bike instance not found."}, status=404)

def reservations(request):
    """Render the reservations page."""
    if request.user.is_authenticated:
        user_reservations = Reservation.objects.filter(user=request.user).order_by("-created_at")

    return render(request, "reservations.html", {
        "reservations": user_reservations
    })

def reservation_delete(request):
    """Render the reservations page."""
    if request.user.is_authenticated:
        if request.method == "POST":
            reservation_id = request.POST.get("reservation_id")
            reservation = get_object_or_404(Reservation, id=reservation_id)
            reservation.delete()
            messages.success(request, "Reservation cancelled successfully.")
            return redirect("reservations")

def reservation_edit(request, reservation_id):
    """Edit an existing reservation."""
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    if request.method == "POST":
        booking_form = EditBookingForm(request.POST, instance=reservation)
        print(booking_form)
        if booking_form.is_valid():
            updated_reservation = booking_form.save(commit=False)
            updated_reservation.start_time = booking_form.cleaned_data["start_time"]
            updated_reservation.end_time = booking_form.cleaned_data["end_time"]
            updated_reservation.save()
            messages.success(request, "Your reservation has been updated successfully!")
            return redirect("reservations")
        else:
            messages.error(request, "Something went wrong. Please check the form for errors.")
    else:
        booking_form = EditBookingForm(instance=reservation)

    return render(request, "reservation-edit.html", {
        "form": booking_form,
        "bike_model": reservation.bike_instance.bike_model,
    })


def routes(request):
    """Render the routes page."""
    return render(request, "routes.html", {})

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
