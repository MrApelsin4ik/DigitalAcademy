# models.py
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="customuser_set",
        related_query_name="user",
        blank=True,
        verbose_name="groups",
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
    )

    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="customuser_set",
        related_query_name="user",
        blank=True,
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
    )


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_participant = models.BooleanField(default=True)
    region = models.CharField(max_length=255, default="", blank=True)
    school_name = models.CharField(max_length=255, default="", blank=True)
    full_name = models.CharField(max_length=255, default="", blank=True)
    age = models.IntegerField(default=None, blank=True, null=True)
    grade_or_course = models.CharField(max_length=255, default="", blank=True)
    organization_name = models.CharField(max_length=255, default="", blank=True)
