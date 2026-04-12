# lexiflow_backend/lexiflow_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from drf_spectacular.utils import extend_schema

# Decorate the token views to include them in the schema
token_obtain_pair_view = extend_schema(
    summary="Obtain JWT token pair",
    description="Login with email and password to receive access and refresh tokens.",
    tags=["auth"]
)(TokenObtainPairView.as_view())

token_refresh_view = extend_schema(
    summary="Refresh JWT access token",
    description="Use the refresh token to obtain a new access token.",
    tags=["auth"]
)(TokenRefreshView.as_view())

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth/', include('users.presentation.urls')),   # registration, profile, preferences
        path('words/', include('words.presentation.urls')),
        path('vocabulary/', include('vocabulary.presentation.urls')),
        path('history/', include('history.presentation.urls')),
        path('analytics/', include('analytics.presentation.urls')),
        # Simple JWT endpoints
        path('auth/token/', token_obtain_pair_view, name='token_obtain_pair'),
        path('auth/token/refresh/', token_refresh_view, name='token_refresh'),
    ])),
    # OpenAPI docs
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]