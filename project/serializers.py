from rest_framework import serializers

from user.serializers import UserSerializer
from worktracker.models.project import Project


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class ProjectMemberSerializer(serializers.Serializer):
    user = UserSerializer()
