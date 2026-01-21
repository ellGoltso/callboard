from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    """
    Разрешает чтение всем.
    Редактирование/удаление - только автору объекта или администратору.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        is_owner = obj.author == request.user
        is_admin = request.user.is_authenticated and (
            request.user.role == "admin" or request.user.is_staff
        )

        return is_owner or is_admin

    def has_permission(self, request, view):
        if request.method == "POST":
            return request.user.is_authenticated
        return True
