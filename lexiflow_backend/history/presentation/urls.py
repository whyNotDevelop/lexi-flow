"""
URL configuration for history app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from history.presentation.views import HistoryViewSet

# Create a router for the ViewSet
router = DefaultRouter()
router.register(r'', HistoryViewSet, basename='history')

urlpatterns = [
    path('', include(router.urls)),
]