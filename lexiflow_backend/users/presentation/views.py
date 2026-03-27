"""
DRF ViewSets for Authentication and User operations.

These views provide REST API endpoints for user registration, profile management,
and preferences.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from users.application.services.auth_service import AuthService
from users.presentation.serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserPreferencesSerializer
)


class AuthViewSet(viewsets.ViewSet):
    """
    ViewSet for authentication and user management operations.

    Provides endpoints for registration, login, profile management, and preferences.
    """

    def __init__(self, auth_service: AuthService = None, **kwargs):
        super().__init__(**kwargs)
        if auth_service is None:
            from users.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
            from users.infrastructure.repositories.preferences_repository_impl import PreferencesRepositoryImpl

            user_repo = UserRepositoryImpl()
            prefs_repo = PreferencesRepositoryImpl()

            auth_service = AuthService(
                user_repo=user_repo,
                prefs_repo=prefs_repo
            )
        self.auth_service = auth_service

    @extend_schema(
        summary="Register new user",
        description="Create a new user account and return authentication tokens.",
        request=UserRegistrationSerializer,
        responses={201: dict}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        Register a new user.

        POST /api/auth/register/
        {
            "email": "user@example.com",
            "password": "password123",
            "full_name": "John Doe"
        }
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = self.auth_service.register_user(
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                full_name=serializer.validated_data.get('full_name')
            )

            if user is None:
                return Response(
                    {"error": "Registration failed - email may already exist"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get Django user model for JWT token generation
            django_user = self.auth_service.user_repo.get_django_user_by_id(user.id)
            if django_user is None:
                return Response(
                    {"error": "User created but authentication setup failed"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Generate JWT tokens
            refresh = RefreshToken.for_user(django_user)
            tokens = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response({
                "user": UserSerializer(user).data,
                "tokens": tokens
            }, status=status.HTTP_201_CREATED)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Registration failed: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Get user profile",
        description="Get the current user's profile information.",
        responses={200: UserSerializer}
    )
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        """
        Get current user profile.

        GET /api/auth/profile/
        """
        user_id = request.user.id

        try:
            user = self.auth_service.get_user(user_id)
            serializer = UserSerializer(user)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"Failed to get profile: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Update user profile",
        description="Update the current user's profile information.",
        request=UserSerializer,
        responses={200: UserSerializer}
    )
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """
        Update user profile.

        PATCH /api/auth/update-profile/
        """
        user_id = request.user.id
        serializer = UserSerializer(data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_user = self.auth_service.update_profile(
                user_id=user_id,
                **serializer.validated_data
            )
            response_serializer = UserSerializer(updated_user)
            return Response(response_serializer.data)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to update profile: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Get user preferences",
        description="Get the current user's preferences.",
        responses={200: UserPreferencesSerializer}
    )
    @action(detail=False, methods=['get'], url_path='preferences', permission_classes=[IsAuthenticated])
    def get_preferences(self, request):
        """
        Get user preferences.

        GET /api/auth/preferences/
        """
        user_id = request.user.id

        try:
            prefs = self.auth_service.get_preferences(user_id)
            serializer = UserPreferencesSerializer(prefs)
            return Response(serializer.data)

        except Exception as e:
            return Response(
                {"error": f"Failed to get preferences: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @extend_schema(
        summary="Update user preferences",
        description="Update the current user's preferences.",
        request=UserPreferencesSerializer,
        responses={200: UserPreferencesSerializer}
    )
    @action(detail=False, methods=['patch'], url_path='preferences', permission_classes=[IsAuthenticated])
    def update_preferences(self, request):
        """
        Update user preferences.

        PATCH /api/auth/preferences/
        """
        user_id = request.user.id
        serializer = UserPreferencesSerializer(data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            updated_prefs = self.auth_service.update_preferences(
                user_id=user_id,
                **serializer.validated_data
            )
            response_serializer = UserPreferencesSerializer(updated_prefs)
            return Response(response_serializer.data)

        except ValueError as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {"error": f"Failed to update preferences: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )