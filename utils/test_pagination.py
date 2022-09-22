from unittest import TestCase

from utils.pagination import make_pagination_range


class TestPagination(TestCase):
    def test_check_make_pagination_range_returns_list(self):
        pagination = make_pagination_range(
            all_pages=list(range(1, 21)),
            divided_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

    # Current page = 3
    def test_check_current_page_change(self):
        pagination = make_pagination_range(
            all_pages=list(range(1, 21)),
            divided_pages=4,
            current_page=3,
        )['pagination']

        self.assertEqual([2, 3, 4, 5], pagination)

        pagination = make_pagination_range(
            all_pages=list(range(1, 21)),
            divided_pages=4,
            current_page=15,
        )['pagination']

        self.assertEqual([14, 15, 16, 17], pagination)

    def test_check_static_pages_in_last_range(self):
        pagination = make_pagination_range(
            all_pages=list(range(1, 21)),
            divided_pages=4,
            current_page=18,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            all_pages=list(range(1, 21)),
            divided_pages=4,
            current_page=19,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            all_pages=list(range(1, 21)),
            divided_pages=4,
            current_page=21,
        )['pagination']

        self.assertEqual([17, 18, 19, 20], pagination)

    def test_check_range_lower_than_divided_pages(self):
        pagination = make_pagination_range(
            all_pages=list(range(1, 3)),
            divided_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2], pagination)

        pagination = make_pagination_range(
            all_pages=list(range(1, 5)),
            divided_pages=4,
            current_page=1,
        )['pagination']

        self.assertEqual([1, 2, 3, 4], pagination)

        pagination = make_pagination_range(
            all_pages=list(range(1, 4)),
            divided_pages=4,
            current_page=3,
        )['pagination']

        self.assertEqual([1, 2, 3], pagination)
