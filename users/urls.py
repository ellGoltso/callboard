from django.urls import path
from .views import CustomUserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path(
        "users/",
        CustomUserViewSet.as_view({"post": "create", "get": "list"}),
        name="users-list",
    ),
    path(
        "users/me/",
        CustomUserViewSet.as_view({"get": "me", "patch": "me", "delete": "me"}),
        name="user-me",
    ),
    path(
        "users/reset_password/",
        CustomUserViewSet.as_view({"post": "reset_password"}),
        name="password_reset",
    ),
    path(
        "users/reset_password_confirm/",
        CustomUserViewSet.as_view({"post": "reset_password_confirm"}),
        name="password_reset_confirm",
    ),
    path("users/login/", TokenObtainPairView.as_view(), name="login"),
    path("users/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
