from django.contrib import admin

from announcements.models import Ad, Review


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):

    list_display = ("title", "price", "author", "created_at")
    list_filter = ("created_at", "author")
    search_fields = ("title", "description", "author__email")
    # Позволяет быстро перейти к автору
    raw_id_fields = ("author",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("ad", "author", "created_at")
    search_fields = ("author__email", "ad__title", "text")
