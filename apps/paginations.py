from rest_framework.pagination import PageNumberPagination, CursorPagination


class CustomCursorPagination(CursorPagination):
    ordering = '-created_at'
