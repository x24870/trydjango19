from django.urls import path

from .views import (
    UserCreateAPIView,
    UserLoginAPIView,
)

app_name = 'accounts'

urlpatterns = [
    path('login/', UserLoginAPIView.as_view(), name='login'),
    path('register/', UserCreateAPIView.as_view(), name='register'),
]