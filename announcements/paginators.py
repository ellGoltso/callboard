from rest_framework.pagination import PageNumberPagination


class AdPagination(PageNumberPagination):
    """Класс пагинации для объявлений, < 5"""

    page_size = 4
    page_size_query_param = "limit"  # GET /ads/?limit=2 вернет 2 объекта
    max_page_size = 4
