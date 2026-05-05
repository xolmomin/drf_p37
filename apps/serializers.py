from rest_framework.fields import empty, ImageField, ListField, CharField, IntegerField
from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.models import Post, Tag, User, Category
from apps.models.posts import CategoryImage


class CategorySerializer(Serializer):
    pk = IntegerField(read_only=True)
    name = CharField(max_length=255, default="Botir")

    def create(self, validated_data):
        return Category.objects.create(**self.validated_data)


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'username'


class UserRegisterModelSerializer(ModelSerializer):
    confirm_password = CharField(write_only=True)

    class Meta:
        model = User
        fields = 'id', 'username', 'first_name', 'email', 'phone', 'password', 'confirm_password'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_phone(self, value:str):
        if not value.startswith('+998'):
            raise ValidationError("Nomer xato")
        return value

    def validate(self, attrs):
        if attrs.get('password') != attrs.pop('confirm_password', None):
            raise ValidationError("Passwords do not match.")
        return attrs


class CategoryImageModelSerializer(ModelSerializer):
    images = ListField(child=ImageField(), required=False)

    class Meta:
        model = CategoryImage
        exclude = ['image']

    def create(self, validated_data):
        images = validated_data.pop('images', [])
        category = validated_data.get('category')
        for image in images:
            CategoryImage.objects.create(category=category, image=image)
        return


class PostModelSerializer(ModelSerializer):
    # likes_count = SerializerMethodField()
    # is_liked = SerializerMethodField()
    # author = HiddenField(default=CurrentUserDefault())
    # tags = ListSerializer(child=CharField(max_length=25), write_only=True)

    class Meta:
        model = Post
        fields = 'id', 'title',  # 'content', 'author', 'category', 'is_published', 'tags', 'views_count', 'likes_count', 'is_liked'
        # read_only_fields = ('views_count',)

    def __init__(self, instance=None, data=empty, **kwargs):
        fields = kwargs['context']['request'].query_params.get('fields')
        super().__init__(instance, data, **kwargs)
        if fields:
            allowed = set(fields.split(','))
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_likes_count(self, obj: Post):
        # return Like.objects.filter(post=obj).count()
        return obj.likes_count

    def get_is_liked(self, obj: Post):
        # request = self.context.get('request')
        # user = request.user
        # if user.is_authenticated:
        #     return Like.objects.filter(post=obj, user=user).exists()
        # return False
        return obj.is_liked

    def _check_tag(self, validated_data):
        tags = validated_data.pop('tags', [])
        tag_list = []
        for tag in tags:
            obj, created = Tag.objects.get_or_create(name=tag)
            tag_list.append(obj)

        return tag_list

    def create(self, validated_data):
        tag_list = self._check_tag(validated_data)
        instance: Post = super().create(validated_data)
        instance.tags.set(tag_list)
        return instance

    def update(self, instance, validated_data):
        tag_list = self._check_tag(validated_data)
        instance.tags.set(tag_list)
        return super().update(instance, validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        data = cls.token_class.for_user(user)
        data.payload['role'] = user.role
        return data
