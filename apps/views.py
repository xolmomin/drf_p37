from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from apps.models import Post, Comment
from apps.serializers import PostModelSerializer, CommentModelSerializer


@extend_schema(tags=['Post'])
class PostListCreateAPIView(ListCreateAPIView):
    queryset = Post.objects.order_by('-id')
    serializer_class = PostModelSerializer


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


# django filters, pagination
# https://www.django-rest-framework.org/api-guide/serializers/#declaring-serializers
# serializers
# jwt
