import django_filters as dj_filt
from reviews.models import Title


class TitleFilter(dj_filt.FilterSet):
    name = dj_filt.CharFilter(
        field_name='name', lookup_expr='icontains'
    )
    year = dj_filt.NumberFilter(field_name='year')
    genre = dj_filt.CharFilter(field_name='genre__slug')
    category = dj_filt.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category',)
