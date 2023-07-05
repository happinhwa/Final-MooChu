from django import template

register = template.Library()

@register.inclusion_tag('paginator_buttons.html')  # 변경된 데코레이터
def render_paginator_buttons(page_obj):
    page_number = page_obj.number
    paginator = page_obj.paginator

    start = page_number - 5 if page_number - 5 > 0 else 1
    end = page_number + 5 if page_number + 5 <= paginator.num_pages else paginator.num_pages

    pages = []

    if start > 1:
        pages.append((1, False))
        if start > 2:
            pages.append((-1, None))

    for num in range(start, end + 1):
        is_active = num == page_number
        pages.append((num, is_active))

    if end < paginator.num_pages:
        if end < paginator.num_pages - 1:
            pages.append((-1, None))
        pages.append((paginator.num_pages, False))

    return {"rendered_pages": pages}
