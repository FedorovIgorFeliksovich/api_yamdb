from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from users.models import User


class Title():
    pass


class Review(models.Model):
    """Модель для работы с отзывами"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Введите целое число от 1 до 10'),
            MaxValueValidator(10, 'Введите целое число от 1 до 10')
        ], # Указываю таким образом, что поставленная оценка может быть от 0 до 10
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ), # Накладывает ограничение на БД, что пользователь может 
               # оставить лишь 1 отзыв на 1 произведение.
        ]
    
    def __str__(self):
        return f'Оценка {self.author.username} на {self.title.name}'


class Comment(models.Model):
    """Модель для работы с комментариями"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']

    def __str__(self):
        return f'Комментарий {self.author.username} на {self.review.title.name}'