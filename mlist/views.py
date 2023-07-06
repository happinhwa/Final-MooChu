from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import collection, mongodb_collection1, mongodb_collection2, mongodb_collection3
from datetime import datetime
from .utils import render_paginator_buttons
from django.http import Http404

def redirect_to_movie_list(request):
    return redirect('mlist:mlist_page', page_number=1)
#페이지 1으로 바로 리다이렉트하기 위함.

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import collection
from .utils import render_paginator_buttons
def movie_list(request, page_number=None):
    if page_number is None:
        page_number = int(request.GET.get('page', 1))

    total_movies = collection.count_documents({})
    per_page = 20

    if page_number < 1:
        page_number = 1

    movies = collection.find({}, {"overview": 1, "title": 1, "poster_path": 1})
    movies = list(movies)
    paginator = Paginator(movies, per_page)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    url = f"/mlist/page={page_number}/"
    if request.GET.get('page') and int(request.GET['page']) != page_number:
        return redirect(url)

    paginator_buttons = render_paginator_buttons(paginator, page_number)

    context = {
        'movies': page_obj,
        'page_obj': page_obj,
        'total_movies': total_movies,
        'paginator': paginator_buttons
    }

    return render(request, 'mlist/movie_list.html', context)








from datetime import datetime

def c_net(request):
    movies = mongodb_collection1.find({}, {"num": 1, "title": 1, "img_link": 1})

    # Group movies by dday
    dday_groups = {}
    for movie in movies:
        dday = movie['num']
        if dday in dday_groups:
            dday_groups[dday].append(movie)
        else:
            dday_groups[dday] = [movie]

    # Sort the dday groups by dday in ascending order
    sorted_groups = sorted(dday_groups.items(), key=lambda x: x[0])

    # Pagination settings
    per_page = 20  # Set a maximum of 20 movies per page
    page_number = request.GET.get('page', 1)
    paginator = Paginator(sorted_groups, per_page)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'mlist/c_movie.html', context)


def render_paginator_buttons(paginator, current_page):
    page_buttons = []
    start_page = max(1, current_page - 2)
    end_page = min(paginator.num_pages, current_page + 2)

    if start_page > 1:
        page_buttons.append((1, False))
        if start_page > 2:
            page_buttons.append((-1, False))

    for page in range(start_page, end_page + 1):
        is_current = (page == current_page)
        page_buttons.append((page, is_current))

    if end_page < paginator.num_pages:
        if end_page < paginator.num_pages - 1:
            page_buttons.append((-1, False))
        page_buttons.append((paginator.num_pages, False))

    return page_buttons
