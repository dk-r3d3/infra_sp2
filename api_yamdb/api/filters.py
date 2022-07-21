"""High level support for doing this and that."""
import django_filters

from reviews.models import Title


class TitleFilter(django_filters.FilterSet):
    """High level support for doing this and that."""

    name = django_filters.CharFilter(lookup_expr='startswith')
    category = django_filters.CharFilter(field_name='category__slug')
    genre = django_filters.CharFilter(field_name='genre__slug')

    class Meta:
        """High level support for doing this and that."""

        model = Title
        fields = ('category', 'genre', 'name', 'year')
