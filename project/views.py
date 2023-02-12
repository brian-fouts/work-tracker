from django.db.utils import IntegrityError
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request

from project.models import Project, ProjectMember
from work.models import Work
from work.serializers import WorkSerializer

from .serializers import ProjectMemberSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=["post"], name="join-project")
    def join(self, request: Request, pk: int) -> JsonResponse:
        project = self.get_object()
        user = request.user

        try:
            project_member = ProjectMember.objects.create(project=project, user=user)
        except IntegrityError:
            return JsonResponse(
                {"errors": ["You have already joined this project"]},
                status=status.HTTP_409_CONFLICT,
            )

        serializer = ProjectMemberSerializer(project_member)
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"], name="leave-project")
    def leave(self, request: Request, pk: int) -> JsonResponse:
        project = self.get_object()
        user = request.user

        try:
            project_member = ProjectMember.objects.get(project=project, user=user)
        except ProjectMember.DoesNotExist:
            return JsonResponse(
                {"errors": ["You are not a member of this project"]},
                status=status.HTTP_409_CONFLICT,
            )

        project_member.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=["get"], name="list-members")
    def members(self, request: Request, pk: int) -> JsonResponse:
        project = self.get_object()
        members = ProjectMember.objects.filter(project=project)

        context = {"request": request}

        serializer = ProjectMemberSerializer(members, many=True, context=context)
        return JsonResponse(serializer.data, safe=False)

    @action(detail=True, methods=["get"], name="list-work")
    def work(self, request: Request, pk: int) -> JsonResponse:
        project = self.get_object()
        user = request.user

        try:
            ProjectMember.objects.get(project=project, user=user)
        except ProjectMember.DoesNotExist:
            return JsonResponse(
                {"errors": ["You are not a member of this project"]},
                status=status.HTTP_403_FORBIDDEN,
            )

        works = Work.objects.filter(project=project)

        serializer = WorkSerializer(works, many=True)
        return JsonResponse(serializer.data, safe=False)
