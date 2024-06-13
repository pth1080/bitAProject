import http


def response_paginate(data_response: list, page: int, page_size: int, total_items: int):
    # Calculate the total number of full pages
    total_pages = total_items // page_size
    # If there are remaining items, add a page
    if total_items % page_size != 0:
        total_pages += 1
    return {
        'page': page,
        'page_size': page_size,
        'data': data_response,
        'count': len(data_response),
        'total_records': total_items,
        'total_pages': total_pages,
        'status_code': http.HTTPStatus.OK
    }
