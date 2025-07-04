from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("bikes/", views.bikes, name="bikes"),
    path("reservations/", views.reservations, name="reservations"),
    path("contact/", views.contact, name="contact"),
    path("routes/", views.routes, name="routes"),
    path("login/", views.login, name="login"),
    path("register/", views.register, name="register"),
]