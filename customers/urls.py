from django.urls import path, include
from rest_framework import routers

from .views import RegisterView, LoginView, CheckAuthView, TokenRefreshView


urlpatterns = [
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('auth/check-auth/', CheckAuthView.as_view(), name='check-auth'),
    path('auth/refresh-token/', TokenRefreshView.as_view(), name='token_refresh'),
]

