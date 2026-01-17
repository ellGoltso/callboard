import pytest
from django.urls import reverse
from announcements.models import Ad, Review
from django.contrib.auth import get_user_model


@pytest.mark.django_db
class TestAds:
    def test_list_ads_anonymous(self, api_client):
        """Аноним может просматривать список объявлений"""
        url = reverse('announcements:ads-list')
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_ad_authenticated(self, api_client, test_user):
        """Авторизованный пользователь может создать объявление"""
        api_client.force_authenticate(user=test_user)
        url = reverse('announcements:ads-list')
        data = {"title": "iPhone 15", "price": 100000, "description": "New"}
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert Ad.objects.count() == 1

    def test_update_foreign_ad_forbidden(self, api_client, test_user, admin_user):
        """Обычный пользователь не может редактировать чужое объявление"""
        ad = Ad.objects.create(title="MacBook", price=200, author=admin_user)

        api_client.force_authenticate(user=test_user)
        url = reverse('announcements:ads-detail', args=[ad.id])
        response = api_client.patch(url, {"title": "Hacked"})
        assert response.status_code == 403

    def test_admin_can_delete_any_ad(self, api_client, admin_user, test_user):
        """Админ может удалить объявление любого пользователя"""
        ad = Ad.objects.create(title="User Ad", price=10, author=test_user)

        api_client.force_authenticate(user=admin_user)
        url = reverse('announcements:ads-detail', args=[ad.id])
        response = api_client.delete(url)
        assert response.status_code == 204
        assert Ad.objects.count() == 0

    def test_search_ad_by_title(self, api_client, test_user):
        """Проверка поиска по названию"""
        Ad.objects.create(title="Xiaomi", price=10, author=test_user)
        Ad.objects.create(title="Samsung", price=10, author=test_user)

        url = reverse('announcements:ads-list')
        response = api_client.get(url, {"search": "Xiaomi"})
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['title'] == "Xiaomi"


@pytest.mark.django_db
def test_create_review(api_client, test_user):
    ad = Ad.objects.create(title="Test Ad", price=100, author=test_user)
    api_client.force_authenticate(user=test_user)

    url = reverse('announcements:ad-reviews', args=[ad.id])
    response = api_client.post(url, {"text": "Great item!"})

    assert response.status_code == 201
    assert Review.objects.count() == 1
    assert Review.objects.first().ad == ad


@pytest.mark.django_db
def test_retrieve_reviews_for_specific_ad(api_client, test_user):
    user1 = test_user
    User = get_user_model()
    user2 = User.objects.create_user(email="user2@test.com", first_name="P", last_name="S", phone="124", password="p")

    ad1 = Ad.objects.create(title="Ad 1", price=100, author=user1)
    ad2 = Ad.objects.create(title="Ad 2", price=200, author=user2)

    Review.objects.create(text="Review 1 for Ad 1", author=user1, ad=ad1)
    Review.objects.create(text="Review 2 for Ad 2", author=user2, ad=ad2)

    api_client.force_authenticate(user=user1)

    url = reverse('announcements:ad-reviews', args=[ad1.id])
    response = api_client.get(url)

    assert response.status_code == 200

    assert len(response.data['results']) == 1
    assert response.data['results'][0]['text'] == "Review 1 for Ad 1"