from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import UserRole


class AuthorOrAdminOrModeratorOrReadOnly(BasePermission):
    """
    Предоставление прав доступа для авторов, модератора
    и администратора на изменение отзывов и комментариев.
    """
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS
                or (request.user.role in [UserRole.ADMIN, UserRole.MODERATOR])
                or obj.author == request.user)


class IsAdminOrIsSuperuserOrReadOnly(BasePermission):
    """
    Права доступа для админа, суперюзера и только для чтения.
    """
    message = 'Доступно только администратору'

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.role == UserRole.ADMIN
            or request.user.is_superuser
        )


# пока только не понятно зачем все эти ограничения
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
