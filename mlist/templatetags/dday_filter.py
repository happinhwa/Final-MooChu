from django import template
from datetime import datetime


# d -day 표시를 위한 filter
register = template.Library()

@register.filter
def dday(value):
    today = datetime.now().date()
    dday = (datetime.strptime(value, '%y.%m.%d').date() - today).days
    return f'D-{dday}'