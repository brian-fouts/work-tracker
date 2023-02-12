from django.db import models

from project.models import Project
from user.models import User


class Work(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    start_time = models.DateTimeField()
    duration = models.FloatField()
