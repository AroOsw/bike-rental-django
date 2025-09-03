from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("bikes/<str:slug>", views.bikes, name="bikes"),
    path("bike-details/<str:slug>", views.bike_details, name="bike_details"),
    path("reservations/", views.reservations, name="reservations"),
    path("reservation-edit/<int:reservation_id>", views.reservation_edit, name="reservation_edit"),
    path("reservation-delete/", views.reservation_delete, name="reservation_delete"),
    path("api/bike-reservations/<int:bike_instance_id>", views.get_bike_reservations, name="get_bike_reservations"),
    path('api/calculate-price/<int:bike_model_id>/', views.calculate_price_ajax, name='calculate_price_ajax'),
    path("contact/", views.contact, name="contact"),
    path("routes/", views.routes, name="routes"),
    path("terms/", views.terms, name="terms"),
    path("profile/", views.profile, name="profile"),
    # path("logout_user/", views.logout_user, name="logout_user"),
]