from rest_framework import viewsets, filters, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from reviews.models import Review, Title, Category, Genge
from .filters import TitleFilter
from .permissions import ReviewPermission
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    CategorySerializer,
    CommentSerializer, 
    ReviewSerializer,
    GenreSerializer,
    TitleSerializerRead,
    TitleSerializerCre5ate,
)

class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""
    serializer_class = ReviewSerializer #Указываем серилизатор с которым будет 
    # работать вьюха
    permission_classes = (ReviewPermission,) #даю разрешения на основе Permission
    # авторизованным пользователям, а так же админу, суперпользователю и автору

    def get_queryset(self): #динамическое определение доступных запросов
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer): #Создание объекта
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)

class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями."""
    serializer_class = CommentSerializer
    permission_classes = (ReviewPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)


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
