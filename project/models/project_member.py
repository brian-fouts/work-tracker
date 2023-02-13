import logging
from typing import Optional, Union

from django.conf import settings
from django.core.cache import cache
from django.db import models

from project.models import Project
from user.models import User


class ProjectMemberCache:
    @classmethod
    def get_cache_key(cls, project_id: int, user_id: int) -> str:
        return f"project-member-{project_id}-{user_id}"

    @classmethod
    def get(cls, project_id: int, user_id: int) -> Union["ProjectMember", None]:
        cache_key = cls.get_cache_key(project_id, user_id)
        result = cache.get(cache_key)

        if result:
            logging.debug(f"CACHE HIT: {cache_key}")
        else:
            logging.debug(f"CACHE MISS: {cache_key}")
        return result

    @classmethod
    def set(cls, project_id: int, user_id: int, obj: "ProjectMember") -> None:
        cache_key = cls.get_cache_key(project_id, user_id)
        logging.debug(f"CACHE SET: {cache_key}")
        cache.set(cache_key, obj, settings.PROJECT_MEMBER_CACHE_TTL)

    @classmethod
    def invalidate(cls, project_id: int, user_id: int) -> None:
        cache_key = cls.get_cache_key(project_id, user_id)
        logging.debug(f"CACHE DELETE: {cache_key}")
        cache.delete(cache_key)


class ProjectMemberManager(models.Manager):
    """
    Reduces Database requests when fetching a object by project and user
    """

    def get(
        self, *args, project: Optional[Project] = None, user: Optional[User] = None, **kwargs
    ) -> Union["ProjectMember", None]:
        if not project or not user:
            return super().get(*args, project=project, user=user, **kwargs)

        project_member = ProjectMemberCache.get(project.id, user.id)
        if not project_member:
            project_member = super().get(project=project, user=user)
            ProjectMemberCache.set(project.id, user.id, project_member)

        return project_member


class ProjectMember(models.Model):
    class Meta:
        unique_together = ["project", "user"]

    objects = ProjectMemberManager()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def delete(self, *args, **kwargs):
        ProjectMemberCache.invalidate(self.project.id, self.user.id)
        return super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        result = super().save(*args, **kwargs)
        ProjectMemberCache.set(self.project.id, self.user.id, self)
        return result
