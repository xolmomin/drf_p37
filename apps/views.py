from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView

from apps.models import Post, Comment, User
from apps.serializers import PostModelSerializer, CommentModelSerializer, UserDetailModelSerializer, \
    UserModelSerializer, UserCreateModelSerializer


@extend_schema(tags=['User'])
class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.order_by('-id')
    serializer_class = UserModelSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return UserCreateModelSerializer
        return super().get_serializer_class()


@extend_schema(tags=['User'])
class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.order_by('-id')
    serializer_class = UserDetailModelSerializer
    lookup_field = 'username'


@extend_schema(tags=['Post'])
class PostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.order_by('-id')
    serializer_class = PostModelSerializer
    filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('userId',)
    # filterset_class = PostFilter


@extend_schema(tags=['Post'])
class PostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostModelSerializer


@extend_schema(tags=['Post'])
class PostCommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        pk = self.kwargs.get('pk')
        return qs.filter(postId=pk)


@extend_schema(tags=['Comment'])
class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_fields = ('postId', 'email')
    search_fields = ('email', 'name')
    ordering_fields = ('id', 'postId')
