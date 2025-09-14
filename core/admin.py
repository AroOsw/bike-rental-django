from django.contrib import admin
from .models import BikeInstance, BikeModel, Reservation, ChatMessage, Profile, StravaActivity
# Register your models here.

@admin.register(BikeInstance)
class BikeInstanceAdmin(admin.ModelAdmin):
    list_display = ["bike_model", "size", "serial_number", "status"]

admin.site.register(BikeModel)
admin.site.register(Reservation)
admin.site.register(ChatMessage)
admin.site.register(Profile)
admin.site.register(StravaActivity)
