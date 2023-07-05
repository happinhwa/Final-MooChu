from django import template
from datetime import datetime

register = template.Library()

@register.filter
def dday(value):
    today = datetime.now().date()
    dday = (datetime.strptime(value, '%y.%m.%d').date() - today).days
    return f'D-{dday}'