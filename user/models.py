import logging

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import UserManager as BaseUserManager
from django.core.cache import cache


class UserCache:
    @classmethod
    def get_cache_key(cls, user_id):
        return f"auth-user-{user_id}"

    @classmethod
    def get(cls, user_id):
        cache_key = cls.get_cache_key(user_id)
        result = cache.get(cache_key)

        if result:
            logging.debug(f"CACHE HIT: {cache_key}")
        else:
            logging.debug(f"CACHE MISS: {cache_key}")
        return result

    @classmethod
    def set(cls, user_id, obj):
        cache_key = cls.get_cache_key(user_id)
        logging.debug(f"CACHE SET: {cache_key}")
        return cache.set(cache_key, obj, settings.USER_CACHE_TTL)


class UserManager(BaseUserManager):
    """
    Instruments caching layer when fetching a single object
    """

    def get(self, *args, **kwargs):
        if "id" not in kwargs:
            return super().get(*args, **kwargs)

        user_id = kwargs["id"]
        user = UserCache.get(user_id)
        if not user:
            user = super().get(id=user_id)
            UserCache.set(user_id, user)

        return user


class User(AbstractUser):
    class Meta:
        db_table = "auth_user"

    objects = UserManager()
