from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


# class Project(models.Model):
    # project_text = models.CharField(max_length=20)


class Todo(models.Model):
    event_text = models.CharField(max_length=200)
    description = models.CharField(max_length=300, default='')
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # project = models.ForeignKey(Project, on_delete=models.CASCADE, default='default')


class Done(models.Model):
    done_text = models.CharField(max_length=200)
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    # done_project = models.ForeignKey(Project, on_delete=models.CASCADE, default='default')


class Subtasks(models.Model):
    subtask_text = models.CharField(max_length=200)
    main_task = models.ForeignKey(Todo, on_delete=models.CASCADE)
