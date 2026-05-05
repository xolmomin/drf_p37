from django.db.models import Model, ForeignKey, CASCADE, ManyToManyField, ImageField
from django.db.models.fields import CharField, TextField, DateTimeField, PositiveIntegerField, BooleanField
from django_ckeditor_5.fields import CKEditor5Field


class Category(Model):
    name = CharField(max_length=255)


class CategoryImage(Model):
    category = ForeignKey('apps.Category', CASCADE, related_name='images')
    image = ImageField(upload_to='category/images/%Y/%m/%d', blank=True, null=True)


class Tag(Model):
    name = CharField(max_length=255)


class Post(Model):
    title = CharField(max_length=255)
    content = CKEditor5Field(blank=True)
    author = ForeignKey('apps.User', CASCADE, related_name='posts')
    category = ForeignKey('apps.Category', CASCADE, related_name='posts')
    is_published = BooleanField(db_default=True)
    tags = ManyToManyField('apps.Tag', blank=True, related_name='posts')
    views_count = PositiveIntegerField(db_default=0)
    created_at = DateTimeField(auto_now=True)


class Like(Model):
    user = ForeignKey('apps.User', CASCADE, related_name='likes')
    post = ForeignKey('apps.Post', CASCADE, related_name='likes')

    class Meta:
        unique_together = (
            ('user', 'post'),
        )
