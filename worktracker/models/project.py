from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=50)


class ProjectMember(models.Model):
    project = models.ManyToManyField(Project)
    user = models.ManyToManyField(User)


