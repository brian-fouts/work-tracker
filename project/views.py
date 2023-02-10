from django.db.utils import IntegrityError
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.request import Request

from worktracker.models.project import Project, ProjectMember

from .serializers import ProjectMemberSerializer, ProjectSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    @action(detail=True, methods=["post"], name="join-project")
    def join(self, request: Request, pk: int) -> JsonResponse:
        project = self.get_object()
        user = request.user

        project_member = ProjectMember(project=project, user=user)
        try:
            project_member.save()
        except IntegrityError:
            return JsonResponse({"errors": ["You have already joined this project"]}, status=409)

        serializer = ProjectMemberSerializer(project_member)
        return JsonResponse(serializer.data, status=201)

    @action(detail=True, methods=["post"], name="leave-project")
    def leave(self, request: Request, pk: int) -> JsonResponse:
        project = self.get_object()
        user = request.user

        try:
            project_member = ProjectMember.objects.get(project=project, user=user)
        except ProjectMember.DoesNotExist:
            return JsonResponse({"errors": ["You are not a member of this project"]}, status=409)

        project_member.delete()
        return JsonResponse({}, status=204)

    @action(detail=True, methods=["get"], name="list-members")
    def members(self, request: Request, pk: int) -> JsonResponse:
        project = self.get_object()
        members = ProjectMember.objects.filter(project=project)

        context = {"request": request}

        serializer = ProjectMemberSerializer(members, many=True, context=context)
        return JsonResponse(serializer.data, status=200, safe=False)
