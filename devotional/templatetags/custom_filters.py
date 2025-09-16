from django import template
import datetime

register = template.Library()

@register.filter
def custom_date(value):
    if isinstance(value, datetime.datetime):
        day = value.day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]

        return value.strftime(f'%d{suffix}, %B %Y')
    return value
