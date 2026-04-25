from django.contrib.admin import actions
from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.filters import PostFilter
from apps.models import Post
from apps.models.posts import Like
from apps.serializers import PostModelSerializer, CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    http_method_names = ['get', 'post']

    @action(detail=True, methods=['post'], url_path='like', serializer_class=None)
    def set_like(self, request, pk=None):
        Like.objects.get_or_create(user=request.user, post_id=pk)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['post'], url_path='unlike', serializer_class=None)
    def set_unlike(self, request, pk=None):
        Like.objects.filter(user=request.user, post_id=pk).delete()
        return Response({'status': 'ok'})

# class PostListCreateAPIView(ListCreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostModelSerializer
#     filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
#     filterset_class = PostFilter
#     ordering_fields = 'created_at', 'views_count', 'likes_count'
#     search_fields = 'title', 'content'
#
#     def get_queryset(self):
#         qs = super().get_queryset()
#         return qs.annotate(likes_count=Count('likes'))
#
#
