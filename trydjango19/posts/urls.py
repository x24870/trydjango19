from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.post_list, name='list'),
    path('create/', views.post_create, name='create'),
    path('<slug>/', views.post_detail, name='detail'),
    path('<id>/update/', views.post_update, name='update'),
    path('<id>/delete/', views.post_delete, name='delete'),
]