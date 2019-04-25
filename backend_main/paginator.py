from rest_framework import pagination

class EventFeedPagination(pagination.PageNumberPagination):
    page_query_param = 'page'