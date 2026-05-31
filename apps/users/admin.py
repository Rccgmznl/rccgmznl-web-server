from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Admin configuration for the custom User model.
    
    Customizes the default Django UserAdmin to use email as the
    authentication field and adds audit fields to the display.
    """

    fieldsets = (
        ("Account Information", {
            "fields": ("email", "password")
        }),
        ("Personal Information", {
            "fields": ("first_name", "last_name")
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            )
        }),
        ("Audit Information", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
        ("Last Login", {
            "fields": ("last_login",),
            "classes": ("collapse",),
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2"),
        }),
        ("Personal Information", {
            "classes": ("wide",),
            "fields": ("first_name", "last_name"),
        }),
    )

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
        "is_active",
        "created_at",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "created_at",
        "groups",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "created_at",
        "updated_at",
        "last_login",
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )
