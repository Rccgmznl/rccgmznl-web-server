from django.contrib.auth.models import UserManager


class CustomUserManager(UserManager):
    """
    Custom user manager that uses email as the unique identifier
    instead of username.
    """

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and save a user with the given email and password.
        
        Args:
            email (str): The user's email address.
            password (str, optional): The user's password.
            **extra_fields: Additional fields for the user model.
            
        Returns:
            User: The created user instance.
            
        Raises:
            ValueError: If email is not provided.
        """
        if not email:
            raise ValueError("The Email field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.
        
        Args:
            email (str): The user's email address.
            password (str): The user's password.
            **extra_fields: Additional fields for the user model.
            
        Returns:
            User: The created superuser instance.
            
        Raises:
            ValueError: If is_staff or is_superuser is not True.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)
