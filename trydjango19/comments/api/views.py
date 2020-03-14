from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)
from rest_framework.generics import(
    ListAPIView, 
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly
)

from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from posts.api.permissions import IsOwnerOrReadOnly

from comments.models import Comment
from .serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    create_comment_serializer,
)

class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name']
    pagination_class = PostPageNumberPagination #PostLimitOffsetPagination

    def get_queryset(self, *args, **kargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kargs)
        queryset_list = Comment.objects.all() # Same meaning as above line
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query) |
                Q(user__first_name__icontains=query) |
                Q(user__last_name__icontains=query)
                ).distinct()

        return queryset_list

class CommenttDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDetailSerializer
    lookup_field = 'pk'

# class PostUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)

# class PostDeleteAPIView(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#     lookup_field = 'slug'

class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    #serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        slug = self.request.GET.get('slug')
        parent_id = self.request.GET.get('parent_id', None)
        return create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user)

    #def perform_create(self, serializer):
    #    serializer.save(user=self.request.user)