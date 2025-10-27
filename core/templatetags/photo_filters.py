# bikes/templatetags/bike_filters.py

import os
from django import template

register = template.Library()

@register.filter
def file_exists(value):
    try:
        if hasattr(value, 'path') and os.path.exists(value.path):
            return value.url
    except Exception:
        pass
    return ''
