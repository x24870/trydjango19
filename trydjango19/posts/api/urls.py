from django.urls import path

from .views import (
    PostListAPIView,
    PostDetailAPIView,
    PostUpdateAPIView,
    PostDeleteAPIView
)

app_name = 'posts'

urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    # path('create/', views.post_create, name='create'),
    path('<slug>/', PostDetailAPIView.as_view(), name='detail'),
    path('<slug>/update/', PostUpdateAPIView.as_view(), name='update'),
    path('<slug>/delete/', PostDeleteAPIView.as_view(), name='delete'),
]