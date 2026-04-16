from django.urls import path

from apps.views import PostListCreateAPIView, CommentListAPIView, PostRetrieveUpdateDestroyAPIView, \
    PostCommentListAPIView

urlpatterns = [
    path('posts', PostListCreateAPIView.as_view()),
    path('posts/<int:pk>', PostRetrieveUpdateDestroyAPIView.as_view()),
    path('posts/<int:pk>/comments', PostCommentListAPIView.as_view()),
    path('comments', CommentListAPIView.as_view())
]
