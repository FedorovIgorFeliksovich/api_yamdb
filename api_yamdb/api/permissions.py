from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrIsSuperuserTitleCategoryGenre(BasePermission):
    """
    Предоставление прав доступа для администратора и супер юзера
    на добавление и удаление категорий, жанров и произведений.
    """
    message = 'Доступно только администратору!'

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated
                and (request.user.role == 'admin'
                     or request.user.is_superuser))


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
                or (request.user.role in ['admin', 'moderator'])
                or obj.author == request.user)


class IsAdminOrIsSuperuser(BasePermission):
    """Права доступа для админа и суперюзера."""
    message = 'Доступно только администратору!'

    def has_permission(self, request, view):
        return (
            request.user.role == 'admin'
            or request.user.is_superuser
        )
