from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.request import Request

from project.models import ProjectMember

from .models import Work
from .serializers import WorkSerializer


def user_belongs_to_project(user_id, project_id):
    try:
        ProjectMember.objects.get(project=project_id, user=user_id)
    except ProjectMember.DoesNotExist:
        return False
    else:
        return True


class WorkViewSet(viewsets.ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

    def list(self, request: Request) -> JsonResponse:
        return JsonResponse({}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def create(self, request: Request) -> JsonResponse:
        request.data["user"] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if not user_belongs_to_project(request.user, serializer.validated_data["project"]):
            return JsonResponse(
                {"errors": ["You are not a member of this project"]},
                status=status.HTTP_403_FORBIDDEN,
            )

        self.perform_create(serializer)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request: Request, pk: int) -> JsonResponse:
        work = self.get_object()
        if not user_belongs_to_project(request.user, work.project):
            return JsonResponse(
                {"errors": ["You are not a member of this project"]},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = WorkSerializer(work)
        return JsonResponse(serializer.data)

    def update(self, request: Request, pk: int) -> JsonResponse:
        request.data["user"] = request.user.id
        work = self.get_object()
        if work.user != request.user.id:
            return JsonResponse(
                {"errors": ["This object does not belong to you"]},
                status=status.HTTP_403_FORBIDDEN,
            )

        if work.project != request.data["project"]:
            if not user_belongs_to_project(request.user, work.project):
                return JsonResponse(
                    {"errors": ["You are not a member of this project"]},
                    status=status.HTTP_403_FORBIDDEN,
                )
        return super().update(request, pk)

    def partial_update(self, request: Request, pk: int) -> JsonResponse:
        request.data["user"] = request.user.id
        work = self.get_object()

        if work.user != request.user.id:
            return JsonResponse(
                {"errors": ["This object does not belong to you"]},
                status=status.HTTP_403_FORBIDDEN,
            )

        if "project" in request.data and work.project != request.data["project"]:
            if not user_belongs_to_project(request.user, work.project):
                return JsonResponse(
                    {"errors": ["You are not a member of this project"]},
                    status=status.HTTP_403_FORBIDDEN,
                )

        return super().partial_update(request, pk)

    def destroy(self, request: Request, pk: int) -> JsonResponse:
        work = self.get_object()
        if work.user != request.user:
            return JsonResponse(
                {"errors": ["This object does not belong to you"]},
                status=status.HTTP_403_FORBIDDEN,
            )

        return super().destroy(request, pk)
