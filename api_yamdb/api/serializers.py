from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.exceptions import ValidationError

from reviews.models import Review, Comment, Title


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с отзывами."""
    author = serializers.SlugRelatedField(
        slug_field='username', 
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name', 
        read_only=True
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'title', 'author', 'score', 'pub_date')
        
    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST': #Делаем проверку при методе post на наличие автора среди отзывов
            if title.reviews.select_related('title').filter(author=author):
                raise ValidationError(
                    'Отзыв можно оставить только один раз!'
                )
        return data

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с комментариями."""
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'review', 'author', 'text', 'pub_date')
