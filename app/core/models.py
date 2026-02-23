from django.db import models   # noqa: F401
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

from django.conf import settings
# Create your models here.

# Custom manager for the User model
# This controls how users are created and saved


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """
        Create, save, and return a new user.

        email → unique email for authentication
        password → user's password (will be hashed)
        extra_fields → additional fields like name, is_staff, etc.
        """
        if not email:
            raise ValueError('User must have an email address.')
        # Create a new user instance using the custom User model
        # self.model refers to the User class
        user = self.model(email=self.normalize_email(email), **extra_fields)

        # Hash the password securely before saving
        # Never store plain-text passwords
        user.set_password(password)

        # Save the user to the database
        # using=self._db ensures correct database is used,
        # (important for multi-db setups)
        user.save(using=self._db)

        # Return the created user object
        return user


    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)
        return user
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Assign the custom user manager to this model
    objects = UserManager()

    # Defines which field is used as the unique identifier for login
    # Default Django uses "username", but here we use "email"
    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe object"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField("Tag")

    def __str__(self):
        return self.title
    
class Tag(models.Model):
    """Tag object"""

    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )

    def __str__(self) :
        return self.name