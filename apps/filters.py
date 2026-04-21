from django.db.models import Count
from django_filters import FilterSet, NumberFilter

from apps.models import Post


class PostFilter(FilterSet):
    comment_count = NumberFilter(method='filter_comment_count')

    class Meta:
        model = Post
        fields = ()

    def filter_comment_count(self, queryset, key, value):
        return queryset.annotate(
            comment_count=Count('comments')
        ).filter(comment_count__gte=value)
