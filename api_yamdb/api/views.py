from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, mixins
from rest_framework.pagination import PageNumberPagination

from reviews.models import Category, Genre, Title
from .filters import TitleFilter

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializerRead,
    TitleSerializerCreate,
)


class CreateDestroyViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializerCreate
    # нужны разрешения - permission_classes

    pagination_class = PageNumberPagination
    # это настройки фильтрации, DjangoFilterBackend из устанавливаемой библиотеки
    # django-filter. подключение возможно как на уровне INSTALLED_APPS в settings.py
    # так и на уровне представления(вьюсета)
    # DjangoFilterBackend поддерживает высоконастраиваемую фильтрацию полей
    # https://django.fun/ru/docs/django-rest-framework/3.12/api-guide/filtering/
    filter_backends = (DjangoFilterBackend,)
    # настройка фильтрации для произведений по полям
    # выносим в отдельный файл и импортируем сюды
    filterset_class = TitleFilter

    def get_serializer_class(self):
        # выбираем сериализацию в зависимости от типа запроса
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead


class CategoryViewSet(CreateDestroyViewSet):
    """Вьюсет для работы с категориями произведений."""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    # нужны разрешения - permission_classes

    # Класс SearchFilter поддерживает простой поиск на основе одного параметра запроса
    # https://django.fun/ru/docs/django-rest-framework/3.12/api-guide/filtering/
    filter_backends = [filters.SearchFilter]
    # filter_backends будет работать в поле:
    search_fields = ['name']
    # по сути по умолчанию поиск производиться по id (ну или pk)
    # но можно указать явно с помощью lookup_field по какому полю производить поиск
    lookup_field = 'slug'


class GenreViewSet(CreateDestroyViewSet):
    """Вьюсет для работы  жанрами."""
    # сразу сортируем по имени для удобства
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    # нужны разрешения - permission_classes

    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'
