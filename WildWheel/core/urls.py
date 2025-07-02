from django.urls import path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("bikes/", views.bikes, name="bikes"),
]