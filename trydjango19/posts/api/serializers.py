from rest_framework.serializers import ModelSerializer

from posts.models import Post

class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title',
            'slug',
            'content',
            'publish',
        ]

class PostDetailSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id',
            'title',
            'slug',
            'content',
            'publish',
        ]


"""
from posts.models import Post
from posts.api.serializers import PostDetailSerializer

data  = {
    'title': 'Yeah buddy',
    'content': 'New content',
    'publish': '2016-2-12',
    'slug': 'yeah-buddu',
}

obj = Post.objects.get(id=3)
new_item = PostSerializer(obj, data=data)
if new_item.is_valid():
    new_item.save()
else:
    print(new_item.errors)

"""