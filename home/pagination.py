from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param= 'page_size'
    max_page_size = 1

    def get_paginated_response(self, data):
        return Response({
            'pagination':{
                'current_page': self.page.number,
                'next_page': self.get_next_link(),
                'previous_page': self.get_previous_link(),
            },
            'results': data
        })
