from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import UserRole


class AuthorOrAdminOrModeratorOrReadOnly(BasePermission):
    """
    Права доступа для автора и аутентифицированного пользователя.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return (
            obj.author == request.user
            or (request.user.is_authenticated
                and request.user.role in [UserRole.ADMIN, UserRole.MODERATOR]))


class IsAdminOrReadOnly(BasePermission):
    """
    Права доступа для админа и только для чтения.
    """
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
        )


class IsAdmin(BasePermission):
    """
    Права доступа только для админа.
    """
    def has_permission(self, request, view):
        result = request.user.is_authenticated and (
            request.user.is_staff or request.user.role == UserRole.ADMIN)
        return result


class IsModerator(BasePermission):
    """
    Права доступа только для модератора.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == UserRole.MODERATOR)


class IsUser(BasePermission):
    """
    Права доступа только для аутентифицированного пользователя.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == UserRole.USER)


class IsSuperUser(BasePermission):
    """
    Права доступа только для суперпользователя, имеющего все права админа.
    """
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_superuser
                or request.user.role == UserRole.ADMIN)
