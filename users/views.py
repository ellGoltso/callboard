from djoser.views import UserViewSet


class CustomUserViewSet(UserViewSet):
    def perform_update(self, serializer):
        if not self.request.user.is_staff and "role" in serializer.validated_data:
            # Удаление ключа из словаря данных, прошедших валидацию,
            # если запрос отправляет не админ и пытается изменить свое поле 'role'
            serializer.validated_data.pop("role")
        super().perform_update(serializer)
