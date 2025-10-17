import io
import os
from datetime import timedelta

import requests
import urllib3
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.db.models import Max
from core.models import BikeModel, BikeInstance, Reservation, Profile, StravaActivity
from .forms import BookingForm, EditBookingForm, ProfileForm
from django.http import JsonResponse, HttpResponse, FileResponse
from dotenv import load_dotenv
from .utils import generate_gpx_file





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
    return render(request, "reservations.html", {})

def reservation_delete(request):
    """Render the reservations page."""
    if request.user.is_authenticated:
        if request.method == "POST":
            reservation_id = request.POST.get("reservation_id")
            reservation = get_object_or_404(Reservation, id=reservation_id)
            reservation.delete()
            messages.success(request, "Reservation cancelled successfully.")
            return redirect("reservations")
    return redirect("index")

def reservation_edit(request, reservation_id):
    """Edit an existing reservation."""
    if request.user.is_authenticated:
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
        if request.method == "POST":
            booking_form = EditBookingForm(request.POST, instance=reservation)
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
    return redirect("index")

load_dotenv()
STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")
STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")

def refresh_strava_token():
    auth_url = "https://www.strava.com/oauth/token"
    payload = {
        "client_id": STRAVA_CLIENT_ID,
        "client_secret": STRAVA_CLIENT_SECRET,
        "refresh_token": STRAVA_REFRESH_TOKEN,
        "grant_type": "refresh_token",
        "f": "json",
    }

    try:
        response = requests.post(auth_url, data=payload)
        response.raise_for_status()
        data = response.json()

        new_access_token = data.get("access_token")
        new_refresh_token = data.get("refresh_token")

        if  new_access_token and new_refresh_token:
            os.environ["STRAVA_ACCESS_TOKEN"] = new_access_token
            os.environ["STRAVA_REFRESH_TOKEN"] = new_refresh_token
            print("Tokens were updated")
            return True
        else:
            print("Error during token refreshing")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error during token refreshing: {e}")
        return False

def get_strava_activities():
    activities_url = "https://www.strava.com/api/v3/athlete/activities"
    header = {"Authorization": "Bearer " + os.getenv("STRAVA_ACCESS_TOKEN")}
    param = {"per_page": 100, "page": 1}
    response = requests.get(activities_url, headers=header, params=param)
    return response

def routes(request):
    """Render the routes page."""
    last_update_info = StravaActivity.objects.aggregate(Max("updated_at"))
    last_updated_at = last_update_info["updated_at__max"]

    if last_updated_at is None or (timezone.now() - last_updated_at) > timedelta(hours=24):
        try:
            response = get_strava_activities()
            if response.status_code == 401:
                if refresh_strava_token():
                    response = get_strava_activities()
                else:
                    return HttpResponse("Couldn't refresh token, please try again.", status=401)

            response.raise_for_status()
            activities = response.json()

            for activity in activities:
                if activity["type"] == "Ride":
                    summary_polyline = activity.get("map", {}).get("summary_polyline", "")

                    StravaActivity.objects.update_or_create(
                        activity_id=activity["id"],
                        defaults={
                            "name": activity["name"],
                            "distance": float(activity["distance"]/1000),
                            "total_elevation": activity["total_elevation_gain"],
                            "start_date": activity["start_date"],
                            "activity_type": activity["type"],
                            "summary_polyline": summary_polyline,
                        }
                    )

        except requests.exceptions.RequestException as e:
            return HttpResponse(f"Couldn't download activities.{e}", status=500)

    activities = StravaActivity.objects.filter(distance__gte=30).order_by("-start_date")[:9]

    return render(request, "routes.html", {"activities": activities})

def download_gpx(request, id):
    activity = get_object_or_404(StravaActivity, id=id)
    gpx_object = generate_gpx_file(activity.summary_polyline)

    if gpx_object is None:
        return HttpResponse("No data do generate GPX file", status=404)
    gpx_to_xml = gpx_object.to_xml()
    gpx_file = io.BytesIO(gpx_to_xml.encode("utf-8"))
    response = FileResponse(gpx_file, as_attachment=True, filename=f"activity_{id}.gpx")

    return response


def contact(request):
    """Render the contact page."""
    return render(request, "contact.html", {})

def terms(request):
    """Render the terms of service page."""
    return render(request, "terms.html", {})

@login_required
def profile(request):
    """Render the user profile page."""
    user_profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        username = request.POST.get("username")
        if User.objects.filter(username=username).exists():
            messages.error(request, "This username already exists")
            return redirect("profile")

        profile_form = ProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your data has been updated successfully")
            return redirect("profile")
        else:
            messages.error(request, "Error")
    else:
        profile_form = ProfileForm(instance=request.user.profile, user=request.user)
    return render(request, "profile.html", {"form": profile_form})

def logout_view(request):
    """Log out the user and redirect to the index page."""
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("index")
