# yourapp/templatetags/date_extras.py
from django import template

register = template.Library()

@register.filter
def format_with_suffix(value):
    if not value:
        return ""
    day = value.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return value.strftime(f"%A {day}{suffix}, %B, %Y")
