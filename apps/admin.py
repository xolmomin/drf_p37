from django.contrib import admin

from apps.models import Comment


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'postId']
