"""
URL configuration for words app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from words.presentation.views import WordViewSet

# Create a router for the ViewSet
router = DefaultRouter()
router.register(r'', WordViewSet, basename='word')

urlpatterns = [
    path('', include(router.urls)),
]