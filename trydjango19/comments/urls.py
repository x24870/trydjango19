from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('<id>/', views.comment_thread, name='thread'),
    path('<id>/delete/', views.confirm_delete, name='delete'),
]