from django.conf import settings
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.users.models import User
from apps.users.serializers import (
    ChangePasswordSerializer,
    CustomTokenObtainPairSerializer,
    TokenRefreshSerializer,
    UserProfileUpdateSerializer,
    UserRegistrationSerializer,
    UserSerializer,
)


class AuthViewSet(ViewSet):
    """
    ViewSet for authentication-related endpoints.
    
    Provides user registration, password change, logout,
    and user profile management.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        summary="User Registration",
        description="Register a new user account with email and password.",
        request=UserRegistrationSerializer,
        responses={
            201: inline_serializer(
                name="RegistrationResponse",
                fields={
                    "id": serializers.IntegerField(),
                    "email": serializers.EmailField(),
                    "first_name": serializers.CharField(),
                    "last_name": serializers.CharField(),
                    "message": serializers.CharField(),
                },
            ),
            400: inline_serializer(
                name="RegistrationError",
                fields={
                    "email": serializers.ListField(child=serializers.CharField()),
                    "password": serializers.ListField(child=serializers.CharField()),
                },
            ),
        },
        tags=["Authentication"],
    )
    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        """
        Register a new user.
        
        Args:
            request: HTTP request with email, password, first_name, last_name.
            
        Returns:
            Response: Created user data with 201 status or errors with 400.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "message": "User registered successfully.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Get/Update User Profile",
        description="Retrieve or update the authenticated user's profile information.",
        request=UserProfileUpdateSerializer,
        responses={
            200: UserSerializer,
            400: inline_serializer(
                name="UpdateError",
                fields={
                    "first_name": serializers.ListField(child=serializers.CharField()),
                    "last_name": serializers.ListField(child=serializers.CharField()),
                },
            ),
            401: inline_serializer(
                name="UnauthorizedProfileError",
                fields={"detail": serializers.CharField()},
            ),
        },
        tags=["Authentication"],
    )
    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[IsAuthenticated],
        url_path="me",
    )
    def profile(self, request):
        """
        Get or update the current authenticated user's profile.
        
        GET: Retrieve current user's profile information.
        PATCH: Update first_name and/or last_name.
        
        Args:
            request: HTTP request from authenticated user.
            
        Returns:
            Response: User profile data.
        """
        if request.method == "GET":
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        elif request.method == "PATCH":
            serializer = UserProfileUpdateSerializer(
                request.user, data=request.data, partial=True
            )
            if serializer.is_valid():
                user = serializer.save()
                return Response(
                    UserSerializer(user).data,
                    status=status.HTTP_200_OK,
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Change Password",
        description="Change the authenticated user's password.",
        request=ChangePasswordSerializer,
        responses={
            200: inline_serializer(
                name="ChangePasswordResponse",
                fields={"message": serializers.CharField()},
            ),
            400: inline_serializer(
                name="ChangePasswordError",
                fields={
                    "old_password": serializers.ListField(child=serializers.CharField()),
                    "new_password": serializers.ListField(child=serializers.CharField()),
                },
            ),
            401: inline_serializer(
                name="UnauthorizedChangePasswordError",
                fields={"detail": serializers.CharField()},
            ),
        },
        tags=["Authentication"],
    )
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="change-password",
    )
    def change_password(self, request):
        """
        Change the current user's password.
        
        Args:
            request: HTTP request with old and new passwords.
            
        Returns:
            Response: Success message or errors.
        """
        serializer = ChangePasswordSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password changed successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary="Logout",
        description="Logout the authenticated user and clear refresh cookie.",
        request=None,
        responses={
            200: inline_serializer(
                name="LogoutResponse",
                fields={"message": serializers.CharField()},
            ),
            400: inline_serializer(
                name="LogoutError",
                fields={"detail": serializers.CharField()},
            ),
            401: inline_serializer(
                name="UnauthorizedLogoutError",
                fields={"detail": serializers.CharField()},
            ),
        },
        tags=["Authentication"],
    )
    @action(
        detail=False,
        methods=["post"],
        permission_classes=[IsAuthenticated],
        url_path="logout",
    )
    def logout(self, request):
        """
        Logout the current authenticated user.
        
        Args:
            request: HTTP request from authenticated user.
            
        Returns:
            Response: Logout success message.
        """
        response = Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK,
        )

        response.delete_cookie(
            key=settings.JWT_REFRESH_COOKIE_NAME,
            path=settings.JWT_REFRESH_COOKIE_PATH,
            samesite=settings.JWT_REFRESH_COOKIE_SAMESITE,
        )

        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token obtain view using email for authentication.
    
    Extends DRF Simple JWT to use email instead of username
    and return additional user data.
    """

    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        summary="Login / Obtain Tokens",
        description=(
            "Authenticate with email and password to obtain an access token. "
            "Refresh token is stored in a secure HttpOnly cookie."
        ),
        request=inline_serializer(
            name="LoginRequest",
            fields={
                "email": serializers.EmailField(
                    help_text="User's email address."
                ),
                "password": serializers.CharField(help_text="User's password."),
            },
        ),
        responses={
            200: inline_serializer(
                name="LoginResponse",
                fields={
                    "access": serializers.CharField(
                        help_text="Access token for API requests."
                    ),
                    "user": UserSerializer,
                },
            ),
            401: inline_serializer(
                name="LoginError",
                fields={"detail": serializers.CharField()},
            ),
        },
        tags=["Authentication"],
    )
    def post(self, request, *args, **kwargs):
        """
        Handle POST request for token generation.
        
        Args:
            request: HTTP request with email and password.
            
        Returns:
            Response: Access token and user data, with refresh cookie set.
        """
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK and "refresh" in response.data:
            refresh_token = response.data.pop("refresh")
            max_age = int(
                settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()
            )

            response.set_cookie(
                key=settings.JWT_REFRESH_COOKIE_NAME,
                value=refresh_token,
                max_age=max_age,
                httponly=settings.JWT_REFRESH_COOKIE_HTTPONLY,
                secure=settings.JWT_REFRESH_COOKIE_SECURE,
                samesite=settings.JWT_REFRESH_COOKIE_SAMESITE,
                path=settings.JWT_REFRESH_COOKIE_PATH,
            )

        return response


class TokenRefreshView(APIView):
    """
    View for refreshing JWT access tokens.

    Reads refresh token from secure HttpOnly cookie and returns
    a new access token when valid.
    """

    permission_classes = [AllowAny]

    @extend_schema(
        summary="Refresh Access Token",
        description=(
            "Use refresh token from secure HttpOnly cookie "
            "to obtain a new access token."
        ),
        request=None,
        responses={
            200: inline_serializer(
                name="RefreshResponse",
                fields={
                    "access": serializers.CharField(
                        help_text="New access token."
                    ),
                },
            ),
            401: inline_serializer(
                name="RefreshError",
                fields={"detail": serializers.CharField()},
            ),
        },
        tags=["Authentication"],
    )
    def post(self, request):
        """
        Refresh the access token using refresh token cookie.
        
        Args:
            request: HTTP request with refresh token cookie.
            
        Returns:
            Response: New access token.
        """
        refresh_token = request.COOKIES.get(settings.JWT_REFRESH_COOKIE_NAME)
        if not refresh_token:
            return Response(
                {"detail": "Refresh token cookie not found."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = TokenRefreshSerializer(data={"refresh": refresh_token})
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
