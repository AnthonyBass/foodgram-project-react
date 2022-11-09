from rest_framework.pagination import PageNumberPagination


class CustomPaginationPageSize(PageNumberPagination):
	page_size_query_param = 'limit'
