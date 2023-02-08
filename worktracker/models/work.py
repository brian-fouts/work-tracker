from django.db import models
from django.contrib.auth.models import User

from .project import Project

class Work(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )
    start_time = models.DateTimeField()
    duration = models.FloatField()