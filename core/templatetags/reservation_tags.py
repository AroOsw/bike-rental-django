from django import template

register = template.Library()

@register.filter
def booking_status(value):
    if value:
        return "status-confirmed"
    return "status-pending"