import json

from django.http import JsonResponse
from rest_framework import generics, permissions, viewsets
from rest_framework.decorators import api_view, permission_classes

from worktracker.models.project import Project, ProjectMember

from .forms import ProjectCreateForm
from .serializers import ProjectMemberSerializer, ProjectSerializer


class ProjectMemberViewSet(generics.ListAPIView):
    serializer_class = ProjectMemberSerializer

    def get_queryset(self):
        project_id = self.kwargs.get("id")
        return ProjectMember.objects.filter(project_id=project_id)


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


def decode_post_body(request):
    body = request.body
    return json.loads(body)


@api_view(["POST"])
def create_project(request):
    body = decode_post_body(request)
    form = ProjectCreateForm(body)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors})

    project = Project(name=form.cleaned_data["name"])
    project.save()

    serializer = ProjectSerializer(project)

    return JsonResponse({"project": serializer.data}, status=201)


@api_view(["GET"])
def get_project(request, id):
    try:
        project = Project.objects.get(id=id)
    except Project.DoesNotExist:
        return JsonResponse({"errors": ["Project not found"]}, status=404)

    serializer = ProjectSerializer(project)
    return JsonResponse({"project": serializer.data})


@api_view(["POST"])
def join_project(request, id):
    user = request.user
    project = Project.objects.get(id=id)
    project_member = ProjectMember(project=project, user=user)
    project_member.save()
    serializer = ProjectMemberSerializer(project_member)
    return JsonResponse({"member": serializer.data}, status=201)


@api_view(["POST"])
def leave_project(request, id):
    user = request.user
    project = Project.objects.get(id=id)

    project_member = ProjectMember.objects.get(project=project, user=user)
    project_member.delete()

    return JsonResponse({}, status=204)
