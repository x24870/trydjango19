from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse

from django.conf import settings
from django.db.models.deletion import SET_NULL, CASCADE

# Create your models here.
class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        #comments = Comment.objects.filter(content_type=content_type, object_id=object_id)
        qs = super(CommentManager, self).filter(content_type=content_type, object_id=object_id).filter(parent=None)
        return qs

    def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=slug)
            if obj_qs.exists and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=SET_NULL, null=True)

    #post = models.ForeignKey(Post, on_delete=CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return str(self.content)

    def children(self): #replies
        return Comment.objects.filter(parent=self)

    def get_absolute_url(self):
        return reverse('comments:thread', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('comments:delete', kwargs={'id': self.id})

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True