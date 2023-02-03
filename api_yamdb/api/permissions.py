from rest_framework.permissions import SAFE_METHODS, BasePermission
from users.models import UserRole


class IsAdminOrIsSuperuserTitleCategoryGenre(BasePermission):
    """
    Предоставление прав доступа для администратора и супер юзера
    на добавление и удаление категорий, жанров и произведений.
    """
    message = 'Доступно только администратору!'

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user.is_authenticated:
            return False
        if request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False


class AuthorOrAdminOrModeratorReviewComment(BasePermission):
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


class IsAdminOrIsSuperuser(BasePermission):
    """Права доступа для админа и суперюзера."""
    message = 'Доступно только администратору!'

    def has_permission(self, request, view):
        return (
            request.user.role == UserRole.ADMIN
            or request.user.is_superuser
        )


# class IsModerator(BasePermission):
#     """Права доступа только для модератора и выше по роли."""
#     message = 'Доступно только модератору и выше по роли!'

#     def has_permission(self, request, view):
#         return (request.user.is_authenticated
#                 and request.user.role == UserRole.MODERATOR)
