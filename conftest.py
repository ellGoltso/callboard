import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user():
    return User.objects.create_user(
        email="user@test.com",
        first_name="Ivan",
        last_name="Ivanov",
        phone="123",
        password="password123",
        role="user",
    )


@pytest.fixture
def admin_user():
    return User.objects.create_superuser(
        email="admin@test.com",
        first_name="Admin",
        last_name="Adminov",
        phone="999",
        password="password123",
    )
