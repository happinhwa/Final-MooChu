from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import mongodb_collection, mongodb_collection1, mongodb_collection2, mongodb_collection3
from datetime import datetime

def movie_list(request):
    # Pagination settings
    total_movies = mongodb_collection.count_documents({})
    per_page = min(total_movies, 20)  # Set a maximum of 20 movies per page
    page_number = request.GET.get('page', 1)
    skip_count = (int(page_number) - 1) * per_page 

    movies = mongodb_collection.find({}, {"overview": 1, "title": 1, "poster_path": 1}).skip(skip_count).limit(per_page)

    paginator = Paginator(list(movies), per_page)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'movies': page_obj,
        'page_obj': page_obj,
        'total_movies': total_movies,
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
    return render(request, 'mlist/c_net.html', context)