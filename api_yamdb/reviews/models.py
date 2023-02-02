from django.db import models


class Genre(models.Model):
    """Модель жанров произведений."""
    name = models.CharField(
        max_length=256,
        verbose_name='Наименование жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug пути',
        help_text='Введите данные типа Slug',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Category(models.Model):
    """Модель категорий произведени."""
    name = models.CharField(
        max_length=256,
        # задаём значение по умолчанию, т.к. наличие категории обязательно
        default='--Пусто--',
        verbose_name='Наименование категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Slug пути',
        help_text='Введите данные типа Slug'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    description = models.TextField(
        verbose_name='Описание произведения'
    )
    # PositiveSmallIntegerField объяснён в Review
    year = models.PositiveSmallIntegerField(
        verbose_name='Год создания произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        # может не быть,
        null=True,
        # но т.к. обязательное поле выше в Category устанавливаем занчение по умолчанию
        blank=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        Genre,
        # связь через(through) GenreToTitle
        through='GenreToTitle',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class GenreToTitle(models.Model):
    """Модель связки жанров и произведений"""
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}, {self.genre}'
