from rest_framework.serializers import ModelSerializer

from apps.models import Post, Comment


class PostModelSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
