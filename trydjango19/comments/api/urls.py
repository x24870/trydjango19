from django.urls import path
from . import views

from .views import (
    CommentListAPIView,
    CommentDetailAPIView,
    CommentCreateAPIView,
)

app_name = 'comments'

urlpatterns = [
    path('', CommentListAPIView.as_view(), name='list'),
    path('create/', CommentCreateAPIView.as_view(), name='create'),
    path('<pk>/', CommentDetailAPIView.as_view(), name='thread'),
    # path('<id>/delete/', views.confirm_delete, name='delete'),
]