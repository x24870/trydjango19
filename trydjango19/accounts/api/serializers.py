from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
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
