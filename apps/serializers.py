import datetime
from datetime import timedelta

from django.utils.timezone import now
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from apps.models import Post, Comment, User


class PostModelSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CommentModelSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class UserModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone')


class UserCreateModelSerializer(ModelSerializer):
    confirm_password = CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'level': {'read_only': True}
        }

    def validate_username(self, val):
        if len(val) < 6:
            raise ValidationError('Username kamida 6 ta belgidan iborat bo`lishi shart!')
        return val

    def validate_first_name(self, val: str):
        if not val.lower().replace("g'", '').replace("o'", '').isalpha():
            raise ValidationError('Ism emasku bu!')
        return val

    def validate_phone(self, val: str):
        if val.startswith('+998'):
            return val.removeprefix('+998')
        return val

    def validate_birth_date(self, val):
        if now().year - val.year < 10:
            raise ValidationError('Foydalanuvchi 10 yoshdan katta bo`lishi shart!')
        return val

    def validate(self, attrs: dict):
        confirm_password = attrs.pop('confirm_password')
        password = attrs.get('password')
        if password != confirm_password:
            raise ValidationError('Parollar bir xil emas!')
        return attrs



class UserDetailModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class UserListCreateModelSerializer(ModelSerializer):
    class Meta:
        model = User
        # fields = '__all__'
        exclude = ('registered_at',)
        # read_only_fields = ('id', 'username', 'email', 'phone')
        extra_kwargs = {
            'password': {'write_only': True},
            'birth_date': {'write_only': True},
            'first_name': {'write_only': True},
            'last_name': {'write_only': True},
            'address': {'write_only': True},
            'company': {'write_only': True},
            # 'registered_at': {'write_only': True},
        }
