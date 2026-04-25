from django.db.models import Count
from django_filters import FilterSet, NumberFilter, DateTimeFilter

from apps.models import Post


class PostFilter(FilterSet):
    from_time = DateTimeFilter(field_name='created_at', lookup_expr='gte')
    to_time = DateTimeFilter(field_name='created_at', lookup_expr='lte')
    views_count = NumberFilter(field_name='views_count', lookup_expr='gt')

    class Meta:
        model = Post
        fields = 'category', 'tags'

    #
    # def filter_comment_count(self, queryset, key, value):
    #     return queryset.annotate(
    #         comment_count=Count('comments')
    #     ).filter(comment_count__gte=value)
