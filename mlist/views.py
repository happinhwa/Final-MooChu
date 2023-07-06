from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import collection, mongodb_collection1, mongodb_collection2, mongodb_collection3
from datetime import datetime
from .utils import render_paginator_buttons
from django.http import Http404

def movie_list(request, page_number=None):
    if page_number is None:
        page_number = int(request.GET.get('page', 1))  # 페이지 번호를 정수로 변환

    # Pagination settings
    total_movies = collection.count_documents({})
    per_page = 20

    if page_number < 1:
        page_number = 1

    # Code related to skip count and limit has been removed
    movies = collection.find({}, {"overview": 1, "title": 1, "poster_path": 1})

    movies = list(movies)  # Convert movies to a list
    paginator = Paginator(movies, per_page)

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    print("Current Page Number: ", page_number)

    url = f"/mlist/?page={page_number}"
    if request.GET.get('page'):
        return redirect(url)

    paginator_buttons = render_paginator_buttons(page_obj)

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

#def netflix(request):
#    # Get movies from MongoDB collection
#    movies = mongodb_collection1.find({}, {"dday": 1, "title": 1, "img_link": 1})
#
#    # Group movies by dday
#    n_groups = {}
#    for movie in movies:
#        dday = movie["dday"]
#        if dday in n_groups:
#            n_groups[dday].append(movie)
#        else:
#            n_groups[dday] = [movie]
#
#    # Sort the dday groups in descending order
#    ns_groups = sorted(n_groups.items(), key=lambda x: x[0], reverse=True)
#
#    # Divide each group into subgroups by source
#    n_sources = {}
#    for nday, n_movies in ns_groups:
#        for n_movie in n_movies:
#            source = n_movie["source"]
#            if source in n_sources:
#                n_sources[source][nday] = n_sources[source].get(nday, []) + [n_movie]
#            else:
#                n_sources[source] = {nday: [n_movie]}
#
#    # Make merged Netflix data
#    merged_data = []
#    for nday, ndata in n_sources.items():
#        for nkey, nmovies in sorted(ndata.items(), key=lambda x: x[0], reverse=True):
#            merged_data += [{"dday": f"D-{nday}", "title": n["title"], "img_link": n["img_link"], "source": "Netflix"}
#                            for n in nmovies]
#
#    paginator = Paginator(merged_data, 20)
#    page_number = request.GET.get("page")
#    page_obj = paginator.get_page(page_number)
#
#    context = {"page_obj": page_obj}
#
#    return render(request, "mlist/c_net.html", context)
#
#
#def watcha(request):
#    # Get movies from MongoDB collection
#    movies = mongodb_collection2.find({}, {"dday": 1, "title": 1, "img_link": 1})
#
#    # Group movies by dday
#    w_groups = {}
#    for movie in movies:
#        dday = movie["dday"]
#        if dday in w_groups:
#            w_groups[dday].append(movie)
#        else:
#            w_groups[dday] = [movie]
#
#    # Sort the dday groups in descending order
#    ws_groups = sorted(w_groups.items(), key=lambda x: x[0], reverse=True)
#
#    # Divide each group into subgroups by source
#    w_sources = {}
#    for wday, w_movies in ws_groups:
#        for w_movie in w_movies:
#            source = w_movie["source"]
#            if source in w_sources:
#                w_sources[source][wday] = w_sources[source].get(wday, []) + [w_movie]
#            else:
#                w_sources[source] = {wday: [w_movie]}
#
#    # Make merged Watcha data
#    merged_data = []
#    for wday, wdata in w_sources.items():
#        for wkey, wmovies in sorted(wdata.items(), key=lambda x: x[0], reverse=True):
#            merged_data += [{"dday": f"D-{wday}", "title": w["title"], "img_link": w["img_link"], "source": "Watcha"}
#                            for w in wmovies]
#
#    paginator = Paginator(merged_data, 20)
#    page_number = request.GET.get("page")
#    page_obj = paginator.get_page(page_number)
#
#    context = {"page_obj": page_obj}
#
#    return render(request, "mlist/c_wat.html", context)
#
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
