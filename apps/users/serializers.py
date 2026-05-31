from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    
    Used for reading user data. Includes all public fields
    except password.
    """

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    
    Handles user creation with email and password validation.
    Returns the created user instance and auth tokens.
    """

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="Password must be at least 8 characters long.",
    )
    password_confirm = serializers.CharField(
        write_only=True,
        help_text="Confirmation password for validation.",
    )

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "password_confirm",
        ]
        extra_kwargs = {
            "first_name": {"required": False},
            "last_name": {"required": False},
        }

    def validate(self, data):
        """
        Validate that passwords match.
        
        Args:
            data (dict): The input data.
            
        Returns:
            dict: The validated data.
            
        Raises:
            ValidationError: If passwords don't match.
        """
        if data.get("password") != data.get("password_confirm"):
            raise serializers.ValidationError(
                {"password_confirm": "Passwords do not match."}
            )
        return data

    def validate_email(self, value):
        """
        Validate that email is unique.
        
        Args:
            value (str): The email address.
            
        Returns:
            str: The validated email.
            
        Raises:
            ValidationError: If email already exists.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "A user with this email already exists."
            )
        return value

    def create(self, validated_data):
        """
        Create a new user instance.
        
        Args:
            validated_data (dict): The validated data.
            
        Returns:
            User: The created user instance.
        """
        validated_data.pop("password_confirm")
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data, password=password)
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer that returns additional user data.
    
    Extends the default simplejwt TokenObtainPairSerializer to include
    user information in the token response.
    """

    def get_token(self, user):
        """
        Generate JWT token for user.
        
        Args:
            user (User): The user instance.
            
        Returns:
            RefreshToken: The refresh token.
        """
        token = super().get_token(user)
        
        # Add custom claims
        token["email"] = user.email
        token["full_name"] = user.get_full_name()
        
        return token

    def validate(self, attrs):
        """
        Validate user credentials using email instead of username.
        
        Args:
            attrs (dict): The input attributes.
            
        Returns:
            dict: The validated attributes with tokens.
            
        Raises:
            ValidationError: If credentials are invalid.
        """
        # Extract the configured username field (email) and password.
        username_field = self.username_field
        email = attrs.get(username_field) or attrs.get("username")
        password = attrs.get("password")

        if not email or not password:
            raise serializers.ValidationError(
                {"detail": "Email and password are required."}
            )

        # Authenticate user by the configured username field.
        user = authenticate(username=email, password=password)
        if not user:
            raise serializers.ValidationError(
                {"detail": "Invalid email or password."}
            )

        if not user.is_active:
            raise serializers.ValidationError(
                {"detail": "This user account is disabled."}
            )

        # Generate tokens
        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }

        return data


class TokenRefreshSerializer(serializers.Serializer):
    """
    Serializer for token refresh endpoint.
    
    Handles refresh token validation and returns a new access token.
    """

    refresh = serializers.CharField()

    def validate(self, attrs):
        """
        Validate and refresh the token.
        
        Args:
            attrs (dict): The input attributes.
            
        Returns:
            dict: The new access token.
            
        Raises:
            ValidationError: If refresh token is invalid or expired.
        """
        try:
            refresh = RefreshToken(attrs["refresh"])
        except Exception:
            raise serializers.ValidationError(
                {"detail": "Invalid or expired refresh token."}
            )

        return {
            "access": str(refresh.access_token),
        }


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password.
    
    Validates old password and ensures new passwords match.
    """

    old_password = serializers.CharField(
        write_only=True,
        help_text="The user's current password.",
    )
    new_password = serializers.CharField(
        write_only=True,
        min_length=8,
        help_text="New password must be at least 8 characters long.",
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        help_text="Confirmation for the new password.",
    )

    def validate(self, data):
        """
        Validate that new passwords match.
        
        Args:
            data (dict): The input data.
            
        Returns:
            dict: The validated data.
            
        Raises:
            ValidationError: If new passwords don't match.
        """
        if data.get("new_password") != data.get("new_password_confirm"):
            raise serializers.ValidationError(
                {"new_password_confirm": "New passwords do not match."}
            )
        return data

    def validate_old_password(self, value):
        """
        Validate that old password is correct.
        
        Args:
            value (str): The old password.
            
        Returns:
            str: The validated old password.
            
        Raises:
            ValidationError: If old password is incorrect.
        """
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError(
                "Old password is incorrect."
            )
        return value

    def save(self):
        """
        Save the new password.
        
        Returns:
            User: The updated user instance.
        """
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile information.
    
    Allows users to update first_name and last_name.
    """

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
        ]
        read_only_fields = ["email"]
