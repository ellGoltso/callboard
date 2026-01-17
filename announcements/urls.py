from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .apps import AnnouncementsConfig
from .views import AdViewSet, ReviewViewSet


app_name = AnnouncementsConfig.name

router = DefaultRouter()
router.register(r"ads", AdViewSet, basename="ads")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "ads/<int:ad_pk>/reviews/",
        ReviewViewSet.as_view({"get": "list", "post": "create"}),
        name="ad-reviews",
    ),
    path(
        "ads/<int:ad_pk>/reviews/<int:pk>/",
        ReviewViewSet.as_view(
            {"patch": "partial_update", "delete": "destroy", "get": "retrieve"}
        ),
        name="review-detail",
    ),
]
