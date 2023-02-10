from rest_framework import serializers

from user.serializers import UserSerializer


class ProjectSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class ProjectMemberSerializer(serializers.Serializer):
    user = UserSerializer()
