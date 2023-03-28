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

"""     def get_paginated_response(self, data):
        
        return Response({
            
            #'next': self.get_next_link(),#delete this
            #'previous': self.get_previous_link(),#delete this
            'count': self.page.paginator.count,
            'comments': data
        }) """