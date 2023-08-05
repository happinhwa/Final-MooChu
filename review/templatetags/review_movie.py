from django import template
from review.views import get_movie_data

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



@register.filter
def get_movie_data_by_id(movie_id):
    return get_movie_data(movie_id)