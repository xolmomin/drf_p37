from django.db.models import Model, IntegerField, CharField, TextField, ForeignKey, CASCADE, EmailField, DateField
from django.db.models.fields import DateTimeField


class Post(Model):
    userId = IntegerField()
    title = CharField(max_length=255)
    body = TextField()
    created_at = DateTimeField(auto_now=True)


class Comment(Model):
    postId = ForeignKey('apps.Post', CASCADE, related_name='comments')
    name = CharField(max_length=255)
    email = EmailField(max_length=255)
    body = TextField()


class User(Model):
    username = CharField(max_length=255, unique=True)
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255, null=True, blank=True)
    password = CharField(max_length=255)
    email = EmailField(max_length=255, null=True, blank=True)
    phone = CharField(max_length=15)
    level = CharField(max_length=25, default='Student')
    address = CharField(max_length=255, null=True, blank=True)
    company = CharField(max_length=255, null=True, blank=True)
    birth_date = DateField(null=True, blank=True)
    registered_at = DateTimeField(auto_now=True)
