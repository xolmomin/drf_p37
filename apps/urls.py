from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView

from apps.views import CustomTokenObtainPairView, PostModelViewSet, UserDestroyAPIView, CategoryImageCreateAPIView, \
    CategoryCreateAPIView

router = DefaultRouter()
router.register('posts', PostModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('users/products/<int:pk>', UserDestroyAPIView.as_view()),
    path('users/products', UserDestroyAPIView.as_view()),
    path('category/images', CategoryImageCreateAPIView.as_view()),
    path('category', CategoryCreateAPIView.as_view()),
    # path('users/delete-account', UserDestroyAPIView.as_view()),
    path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('posts', PostListCreateAPIView.as_view(), name='posts'),
]

