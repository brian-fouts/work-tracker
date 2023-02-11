from rest_framework import serializers

from worktracker.models.work import Work


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = "__all__"
