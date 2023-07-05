from django.core.paginator import Paginator


def render_paginator_buttons(paginator, current_page):
    page_numbers = []
    total_pages = paginator.num_pages

    # Calculate page numbers to display
    if total_pages <= 5:
        page_numbers = range(1, total_pages + 1)
    else:
        if current_page <= 3:
            page_numbers = range(1, 6)
        elif current_page >= total_pages - 2:
            page_numbers = range(total_pages - 4, total_pages + 1)
        else:
            page_numbers = range(current_page - 2, current_page + 3)

    # Add ellipsis if needed
    rendered_pages = []
    for i, page_number in enumerate(page_numbers):
        if i > 0 and page_number - rendered_pages[-1][-1] > 1:
            rendered_pages.append((-1, False))
        rendered_pages.append((page_number, current_page == page_number))

    return rendered_pages
