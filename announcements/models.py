from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Ad(models.Model):
    """Модель объявления"""

    title = models.CharField(max_length=255, verbose_name="Название товара")
    price = models.IntegerField(verbose_name="Цена товара")
    description = models.TextField(
        verbose_name="Описание товара", blank=True, null=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ads",
        verbose_name="Автор объявления",
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания"
    )

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Review(models.Model):
    """Модель отзыва"""

    text = models.TextField(verbose_name="Текст отзыва")
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reviews",
        verbose_name="Автор отзыва",
    )
    ad = models.ForeignKey(
        Ad, on_delete=models.CASCADE, related_name="reviews", verbose_name="Объявление"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Дата и время создания"
    )

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Отзыв от {self.author.email} к объявлению {self.ad.title}"
