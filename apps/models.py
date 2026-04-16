from django.db.models import Model, IntegerField, CharField, TextField, ForeignKey, CASCADE, EmailField


class Post(Model):
    userId = IntegerField()
    title = CharField(max_length=255)
    body = TextField()


class Comment(Model):
    postId = ForeignKey('apps.Post', CASCADE, related_name='comments')
    name = CharField(max_length=255)
    email = EmailField(max_length=255)
    body = TextField()
