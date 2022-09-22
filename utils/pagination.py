from math import ceil


def make_pagination(
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

    if stop_range > total_pages:
        start_range -= (stop_range - total_pages)

    pagination = all_pages[start_range:stop_range]

    return {
        'pagination': pagination,
        'page_range': all_pages,
        'qty_pages': divided_pages,
        'current_page': current_page,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }
