from django.contrib import admin
from .models import BikeInstance, BikeModel, Reservation, ChatMessage, PageImages
# Register your models here.

@admin.register(PageImages)
class PageImagesAdmin(admin.ModelAdmin):
    list_display = ('title', 'page_section', 'slug')
    search_fields = ('title', 'page_section')
    list_filter = ('page_section',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(BikeInstance)
class BikeInstanceAdmin(admin.ModelAdmin):
    list_display = ["bike_model", "size", "serial_number", "status"]


admin.site.register(BikeModel)
admin.site.register(Reservation)
admin.site.register(ChatMessage)