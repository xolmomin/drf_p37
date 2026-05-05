from django.contrib import admin

from apps.models import Post


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    pass
