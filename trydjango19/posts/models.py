from django.db import models
from django.db.models.signals import pre_save
from django.db.models.deletion import SET_NULL
from django.urls import reverse
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.utils.text import slugify
from django.utils.safestring import mark_safe

from markdown_deux import markdown
from comments.models import Comment

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() == super(PostManager, self).all()
        return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())


def upload_location(instance, filename):
    return "{}/{}".format(instance.id, filename)

class Post(models.Model):
    title = models.CharField(max_length=120)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=SET_NULL, null=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to=upload_location,
        null=True,
        blank=True,
        height_field='height_field',
        width_field='width_field')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    publish = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = PostManager() # 'objects' is 'Post.objects'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('posts:detail', kwargs={'slug': self.slug})

    def get_markdown(self):
        return mark_safe(markdown(self.content))

    class Meta:
        ordering = ["-timestamp", "-updated"]

    @property
    def comments(self):
        instance = self
        qs = Comment.objects.filter_by_instance(instance)
        return qs

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by('-id')
    exist = qs.exists()
    if exist:
        new_slug = '%s-%s' % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug

def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, sender=Post)