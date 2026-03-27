"""
URL configuration for users/auth app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from users.presentation.views import AuthViewSet

# Create a router for the ViewSet
router = DefaultRouter()
router.register(r'', AuthViewSet, basename='auth')

urlpatterns = [
    path('', include(router.urls)),
]