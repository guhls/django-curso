from math import ceil

from django.core.paginator import Paginator


def make_pagination_range(
    all_pages,
    divided_pages,
    current_page,
):
    middle_range = ceil(divided_pages / 2)

    start_range = current_page - middle_range
    stop_range = current_page + middle_range

    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset

    total_pages = len(all_pages)

    if stop_range > total_pages and total_pages > divided_pages:
        start_range -= (stop_range - total_pages)

    first_page_out_of_range = current_page > middle_range

    if total_pages < divided_pages:
        start_range = 0
        first_page_out_of_range = False

    pagination = all_pages[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': all_pages,
        'qty_pages': divided_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': first_page_out_of_range,
        'last_page_out_of_range': stop_range < total_pages,
    }


def make_pagination(request, query_set, qty_items, qty_pages):
    current_page = request.GET.get('page', 1)

    paginator = Paginator(query_set, qty_items)
    recipes_obj = paginator.get_page(current_page)

    range_pages = make_pagination_range(
        paginator.page_range,
        qty_pages,
        int(current_page),
    )

    return recipes_obj, range_pages
