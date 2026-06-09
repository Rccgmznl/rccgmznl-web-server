from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.users.managers import CustomUserManager


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=False,
        blank=True,
        null=True,
        help_text=_(
            "Optional. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        verbose_name=_("username"),
    )
    """
    Custom user model extending Django's AbstractUser.
    
    Uses email as the primary login field instead of username.
    
    Fields:
        email (EmailField): Unique email address used for authentication.
        created_at (DateTimeField): Timestamp when the user was created.
        updated_at (DateTimeField): Timestamp when the user was last updated.
        is_active (BooleanField): Whether the user account is active.
    """

    email = models.EmailField(unique=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        db_table = "auth_user"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        """String representation of the user."""
        return self.email

    def get_full_name(self):
        """
        Returns the user's full name.
        
        Returns:
            str: The user's full name (first + last name).
        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_short_name(self):
        """
        Returns the user's short name.
        
        Returns:
            str: The user's first name or email if not set.
        """
        return self.first_name or self.email
