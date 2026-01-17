from rest_framework import serializers
from .models import Ad, Review


class AdSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.email")

    class Meta:
        model = Ad
        fields = ("id", "title", "price", "description", "author", "created_at")

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной.")
        return value


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source="author.email")
    ad = serializers.ReadOnlyField(source="ad.id")

    class Meta:
        model = Review
        fields = ("id", "text", "author", "ad", "created_at")
