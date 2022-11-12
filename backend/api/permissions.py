from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Ограничивает неавторизованных пользователей и
    дает доступ авторизованным и администраторам"""

    def has_permission(self, request, view):

        self.t1 = request.method in permissions.SAFE_METHODS
        self.t2 = request.user.is_authenticated
        return self.t1 or self.t2

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user and request.user.is_authenticated:
            return request.user.is_superuser or obj.author == request.user
        return False
