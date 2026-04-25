from rest_framework.fields import IntegerField, SerializerMethodField
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import Post


class PostModelSerializer(ModelSerializer):
    likes_count = SerializerMethodField()

    class Meta:
        model = Post
        fields = 'id', 'title', 'content', 'author', 'category', 'tags', 'is_published', 'views_count', 'likes_count'
        read_only_fields = ('views_count',)

    def get_likes_count(self, obj: Post):
        return obj.likes_count


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        data = cls.token_class.for_user(user)
        data.payload['role'] = user.role
        return data
