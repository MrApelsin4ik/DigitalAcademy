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
    avatar = models.ImageField(upload_to='uploads/', blank=True, null=True)


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    am = models.IntegerField(default=0)


class Directions(models.Model):
    direction = models.CharField(max_length=150)

class Tasks(models.Model):
    name = models.CharField(max_length=255, default="", blank=True)
    description = models.TextField()
    accelcoin_amount = models.IntegerField()
    directions = models.ManyToManyField(Directions, through='DirectionTasks')


class Solved(models.Model):
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="", blank=True)
    description = models.TextField()

class SolvedTaskFile(models.Model):
    solved_task = models.ForeignKey(Solved, on_delete=models.CASCADE)
    file = models.FileField(upload_to='solved_task_files/')

class OwnSolved(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default="", blank=True)
    description = models.TextField()

class FileOwnSolved(models.Model):
    task = models.ForeignKey(OwnSolved, on_delete=models.CASCADE)
    file = models.FileField(upload_to='own_solved_task_files/')

class OwnerTask(models.Model):
    task_id = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class DirectionTasks(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    direction = models.ForeignKey(Directions, on_delete=models.CASCADE)

class TaskFile(models.Model):
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE)
    file = models.FileField(upload_to='task_files/')
