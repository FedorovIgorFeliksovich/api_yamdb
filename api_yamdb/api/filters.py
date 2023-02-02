import django_filters as dj_filt
from reviews.models import Title


class TitleFilter(dj_filt.FilterSet):
    # наследуемся от Filterset для возможности настройки фильтрации по полям
    # переопределяем поля для фильтрации по установленным параметрам

    # CharFilter - Этот фильтр выполняет простые сопоставления символов, используемые с CharField и TextField по умолчанию
    # field_name - Имя поля модели, по которому выполняется фильтрация
    # lookup_expr - это параметр для определения WHERE при запросе к БД и вида поиска, см.по ссылке
    # https://docs.djangoproject.com/en/4.1/ref/models/querysets/#field-lookups:~:text=for%20more%20information.-,icontains,-%C2%B6
    # 'icontains' - добавляет к WHERE оператор ILIKE который ищет по маске БЕЗ учёта регистра
    #  ибо просто contains - это LIKE, а он ищет точное совпадение С учётом регистра
    name = dj_filt.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    # NumberFilter - Фильтры на основе числового значения, используемые с IntegerField, FloatField и DecimalField по умолчанию
    year = dj_filt.NumberFilter(field_name='year')
    # напоминаение теории! Тут в field_name используется разделитель поиска ORM (__)
    # т.е. для поиска по связянной частью с полем
    # в данном случаем фильтрация жанра происходит по slug-полю
    genre = dj_filt.CharFilter(field_name='genre__slug')
    # то же самое
    category = dj_filt.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ['name', 'year', 'genre', 'category']
