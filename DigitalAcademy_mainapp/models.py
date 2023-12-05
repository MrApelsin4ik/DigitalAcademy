from django.db import models

class Participant(models.Model):
    region = models.CharField(max_length=255)
    school_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    age = models.IntegerField()
    grade_or_course = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

class Partner(models.Model):
    organization_name = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
