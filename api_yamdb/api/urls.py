from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpViewSet, TitleViewSet, UserViewSet,
                    access_token)

app_name = 'api'


class NoPutRouter(DefaultRouter):
    """
    Исключаем метод PUT из роутера.
    """
    def get_method_map(self, viewset, method_map):
        bound_methods = super().get_method_map(viewset, method_map)
        if 'put' in bound_methods.keys():
            del bound_methods['put']
        return bound_methods


router_v1 = NoPutRouter()

router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('auth/signup', SignUpViewSet)

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/token/', access_token, name='token'),
]
