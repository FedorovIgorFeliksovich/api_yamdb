from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Title, Category, Genre


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с жанрами произведений."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для работы с категориями произведений."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями только при чтении."""
    # не забываем! переопределение в сериализаторе делается для получения
    # не id (через ForeignKey), а иного представления, например строкового,
    # но здесь мы используем сериализатор для получения вместо id
    # поля 'name' и 'slug'
    category = CategorySerializer(read_only=True)
    # аналогично
    genre = GenreSerializer(many=True, read_only=True)
    # это поле для чтения, связанное с методом get_rating
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'description', 'year', 'category', 'genre', 'rating'
        )
        read_only_fields = ('id',)

    def get_rating(self, obj):
        # так как возвращаем объект произведения, то через related_name=review
        # получаем отзывы на произведение, далее аггрегируем данные через поле 'score'
        # aggregate() по сути создаёт словарь ключём которого является именованый параметр
        # rating, в значением среднеарифметическое(Avg) по полю 'score'
        obj = obj.reviews.all().aggregate(rating=Avg('score'))
        # так как получается словарь, то и значение получаем по ключу
        return obj['rating']


class TitleSerializerCreate(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями при создании."""
    # SlugRelatedField может использоваться для представления цели отношения, используя поле цели
    # по ссылке отлоичный пример для понимания
    # https://ilyachch.gitbook.io/django-rest-framework-russian-documentation/overview/navigaciya-po-api/relations#:~:text=%D0%B0%D1%80%D0%B3%D1%83%D0%BC%D0%B5%D0%BD%D1%82%D0%B0format.-,SlugRelatedField,-SlugRelatedField%20%D0%BC%D0%BE%D0%B6%D0%B5%D1%82%20%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D1%82%D1%8C%D1%81%D1%8F
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        # many - потому что жанров произведения может быть несколько
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'description', 'year', 'category', 'genre')
