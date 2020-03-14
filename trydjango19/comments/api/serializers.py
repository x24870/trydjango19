from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    ModelSerializer, 
    HyperlinkedIdentityField,
    SerializerMethodField,
    ValidationError,
)

from comments.models import Comment

User = get_user_model()

def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                'content',
                'timestamp',
            ]

        def __init__(self, *args, **kwargs):
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count()==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        def validate(self, data):
            model_type = self.model_type
            model_qs = ContentType.objects.all()
            model_exist = False
            SomeModel = None
            for m in model_qs:
                # Django2.2 ContentType __str__ is diffrent from Django 1.9
                # So I have to go through the model query set for find the matching model name
                if m.name == model_type:
                    SomeModel = m
                    model_exist = True
                    break
            if not model_exist:
                raise ValidationError('This is not a valid content type')
            obj_qs = SomeModel.model_class().objects.filter(slug=self.slug)
            # Type of SomeModel is ContentType, it can't access query model directly
            # So we need .model_class() method to get the model class
            if not obj_qs.exists() or obj_qs.count()!=1:
                raise ValidationError('This is not a slug for this content type')
            return data

        def create(self, validated_data):
            # Exampl URL:
            # http://127.0.0.1:8000/api/comments/create/?type=post&slug=pyk2-created-20&parent_id=21
            content = validated_data.get('content')
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first() #Default user, will fix later
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            comment = Comment.objects.create_by_model_type(model_type, slug, content, main_user, parent_obj=parent_obj)
            return comment

    return CommentCreateSerializer

class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'timestamp',
            'reply_count',
        ]

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentChildSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp',
        ]

class CommentDetailSerializer(ModelSerializer):
    replies = SerializerMethodField()
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'content',
            'reply_count',
            'replies',
        ]

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

class CommentEditSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'timestamp',
        ]