"""
URL configuration for vocabulary app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from vocabulary.presentation.views import VocabularyViewSet

# Create a router for the ViewSet
router = DefaultRouter()
router.register(r'', VocabularyViewSet, basename='vocabulary')

urlpatterns = [
    path('', include(router.urls)),
]