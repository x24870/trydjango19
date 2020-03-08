from django.urls import path
from . import views

from .views import (
    CommentListAPIView,
    CommenttDetailAPIView,
)

app_name = 'comments'

urlpatterns = [
    path('', CommentListAPIView.as_view(), name='list'),
    path('<id>/', CommenttDetailAPIView.as_view(), name='thread'),
    # path('<id>/delete/', views.confirm_delete, name='delete'),
]