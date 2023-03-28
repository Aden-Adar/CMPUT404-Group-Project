from rest_framework import pagination
from rest_framework.response import Response

class CustomPageNumberPagination(pagination.PageNumberPagination):
    ''' Default: 1 page, 5 objects'''
    page_size = 5
    page_size_query_param = 'count'
    max_page_size = 100000
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response(data)

