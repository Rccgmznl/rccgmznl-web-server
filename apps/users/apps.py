from django.apps import AppConfig


class AuthConfig(AppConfig):
    """
    Configuration for the authentication app.
    
    Handles:
    - Custom user model
    - JWT authentication
    - User registration and login
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"
    verbose_name = "Authentication"

    def ready(self):
        """
        Import signals when the app is ready.
        """
        import apps.users.signals  # noqa
