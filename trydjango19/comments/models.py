from django.db import models

from django.conf import settings
from django.db.models.deletion import SET_NULL, CASCADE

from posts.models import Post

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)