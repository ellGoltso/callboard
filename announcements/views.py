from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from .models import Ad, Review
from .serializers import AdSerializer, ReviewSerializer
from .permissions import IsOwnerOrAdminOrReadOnly
from .paginators import AdPagination
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


@extend_schema_view(
    list=extend_schema(
        summary="Список объявлений",
        description="Возвращает список объявлений. Пагинация по 4 объекта. Поиск по полю 'title'.",
    ),
)
class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]
    pagination_class = AdPagination

    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("title",)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@extend_schema_view(
    list=extend_schema(
        summary="Получить все отзывы к объявлению",
        parameters=[
            OpenApiParameter(
                "ad_pk",
                OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID объявления",
            )
        ],
    ),
    create=extend_schema(
        summary="Создать новый отзыв",
        parameters=[
            OpenApiParameter(
                "ad_pk",
                OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description="ID объявления",
            )
        ],
    ),
)
class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrAdminOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(ad_id=self.kwargs.get("ad_pk"))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, ad_id=self.kwargs.get("ad_pk"))
