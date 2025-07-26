from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
import math

class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        total_count = self.page.paginator.count
        total_pages = math.ceil(total_count / self.page_size)
        current_page = self.page.number

        return Response({
            'count': total_count,
            'total_pages': total_pages,
            'current_page': current_page,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })
