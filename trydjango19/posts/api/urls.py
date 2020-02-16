from django.urls import path

from .views import (
    PostListAPIView,
    PostDetailAPIView
)

app_name = 'posts'

urlpatterns = [
    path('', PostListAPIView.as_view(), name='list'),
    # path('create/', views.post_create, name='create'),
    path('<slug>/', PostDetailAPIView.as_view(), name='detail'),
    # path('<id>/update/', views.post_update, name='update'),
    # path('<id>/delete/', views.post_delete, name='delete'),
]