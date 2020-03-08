from rest_framework.serializers import ModelSerializer, HyperlinkedIdentityField

from posts.models import Post

post_detail_url = HyperlinkedIdentityField(
    view_name='posts-api:detail',
    lookup_field='slug',
)

class PostListSerializer(ModelSerializer):
    url = post_detail_url
    # delete_url = HyperlinkedIdentityField(
    #     view_name='posts-api:delete',
    #     lookup_field='slug',
    # )
    class Meta:
        model = Post
        fields = [
            'url',
            'title',
            'content',
            'publish',
            # 'delete_url',
        ]

class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'title',
            'slug',
            'content',
            'publish',
        ]

class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            # 'id',
            'title',
            # 'slug',
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