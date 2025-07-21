from django.contrib import admin
from .models import Bike, Reservation, ChatMessage
# Register your models here.


admin.site.register(Bike)
admin.site.register(Reservation)
admin.site.register(ChatMessage)