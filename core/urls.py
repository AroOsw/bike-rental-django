from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bikes/<str:slug>", views.bikes, name="bikes"),
    path("bike-details/<str:slug>", views.bike_details, name="bike_details"),
    # path("category/<str:slug>", views.category, name="category"),
    path("reservations/", views.reservations, name="reservations"),
    path("contact/", views.contact, name="contact"),
    path("routes/", views.routes, name="routes"),
    path("terms/", views.terms, name="terms"),
    path("profile/", views.profile, name="profile"),
    # path("logout_user/", views.logout_user, name="logout_user"),
]