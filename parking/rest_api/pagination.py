from requests import Response
from rest_framework.pagination import (
    CursorPagination,
    LimitOffsetPagination,
    PageNumberPagination,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = "page_size"
    max_page_size = 1000


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 1
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 1000


class CustomCursorPagination(CursorPagination):
    page_size = 5
    cursor_query_param = "cursor"
    ordering = "-id"
