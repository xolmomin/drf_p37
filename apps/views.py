import os

from django.db.models import Exists, OuterRef, Value, BooleanField
from django.db.models.aggregates import Count
from django.http import FileResponse
from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.models import Post, User, Category
from apps.models.posts import Like, CategoryImage
from apps.permissions import IsAuthorOrReadOnly
from apps.serializers import PostModelSerializer, CustomTokenObtainPairSerializer, UserModelSerializer, \
    CategoryImageModelSerializer, CategorySerializer
from root.settings import BASE_DIR


class CategoryCreateAPIView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class CategoryImageCreateAPIView(CreateAPIView):
    queryset = CategoryImage.objects.all()
    serializer_class = CategoryImageModelSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ExcelAPIView(APIView):
    permission_classes = []

    def get(self, request):
        """
           Return a list of all users.
        """
        return FileResponse(open(os.path.join(BASE_DIR, 'lesson.pdf'), 'rb'), as_attachment=True)


class UserDestroyAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    def get_object(self):
        return self.request.user


class CustomViewSet(ViewSet):
    pass


class PostModelViewSet(ModelViewSet):
    queryset = Post.objects.filter()
    serializer_class = PostModelSerializer
    permission_classes = [IsAuthorOrReadOnly]

    # http_method_names = ['get', 'post', 'patch']
    # pagination_class = None

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_authenticated:
            key = Exists(Like.objects.filter(post_id=OuterRef('pk'), user=user))
        else:
            key = Value(False, BooleanField())

        return qs.annotate(
            likes_count=Count('likes'),
            is_liked=key
        )

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     user = self.request.user
    #     qs = qs.annotate(
    #         likes_count=Count('likes')
    #     )
    #
    #     if user.is_authenticated:
    #         qs = qs.annotate(
    #             is_liked=Exists(
    #                 Like.objects.filter(post_id=OuterRef('pk'), user=user)
    #             )
    #         )
    #     else:
    #         qs = qs.annotate(
    #             is_liked=Value(False, BooleanField())
    #         )
    #     return qs

    @action(detail=True, methods=['post'], url_path='like', serializer_class=None)
    def set_like(self, request, pk):
        Like.objects.get_or_create(user=request.user, post_id=pk)
        return Response({'status': 'ok'})

    @action(detail=True, methods=['post'], url_path='unlike', url_name='unlike', serializer_class=None)
    def set_unlike(self, request, pk=None):
        Like.objects.filter(user=request.user, post_id=pk).delete()
        return Response({'status': 'ok'})

    @action(detail=False, methods=['get'], url_path='my-posts', permission_classes=[IsAuthenticated],
            serializer_class=PostModelSerializer)
    def my_posts(self, request):
        user = request.user
        qs = self.get_queryset().filter(author=user)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        response = self.get_serializer(qs, many=True).data
        return self.get_paginated_response(response)

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
