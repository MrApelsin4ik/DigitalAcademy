from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_participant = models.BooleanField(default=True)
    region = models.CharField(max_length=255, default="", blank=True)
    school_name = models.CharField(max_length=255, default="", blank=True)
    full_name = models.CharField(max_length=255, default="", blank=True)
    age = models.IntegerField(default=None, blank=True, null=True)
    grade_or_course = models.CharField(max_length=255, default="", blank=True)
    organization_name = models.CharField(max_length=255, default="", blank=True)
    email = models.CharField(max_length=255, default="")


class Tasks(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)
    description = models.TextField()
