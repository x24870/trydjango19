from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.db.models import Q 

from rest_framework.serializers import (
    CharField,
    ModelSerializer, 
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
    EmailField,
)

User = get_user_model()

class UserCreateSerializer(ModelSerializer):
    email = EmailField(label='Email address')
    email2 = EmailField(label='Comfirm email')
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'email2',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError('This email has already been registered')
        return data

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError('Email must match')

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError('This email has already been registered')

        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data

class UserLoginSerializer(ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    username = CharField(required=False, allow_blank=True)
    email = EmailField(label='Email address', required=False, allow_blank=True)
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'token',
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        user_obj = None
        email = data.get('email', None)
        username = data.get('username', None)
        password = data['password'] # Because we didn't set password Field to allow_blank=True, so this field must has data
        if not email and not username:
            raise ValidationError('A username or email is required to login')
        # email = data['email']
        # user_qs = User.objects.filter(email=email)
        # if user_qs.exists():
        #     raise ValidationError('This email has already been registered')

        user = User.objects.filter(
            Q(email=email) |
            Q(username=username)
        ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__exact='')
        if user.exists() and user.count()==1:
            user_obj = user.first()
        else:
            raise ValidationError('This username/email is not valid')

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError('Incorrect credentials please try again.')

        data['token'] = 'SOME RANDOM TOKEN'

        return data

    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError('Email must match')

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            raise ValidationError('This email has already been registered')

        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        email = validated_data['email']
        user_obj = User(username=username, email=email)
        user_obj.set_password(password)
        user_obj.save()
        return validated_data