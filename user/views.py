import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.request import Request

from .forms import UserCreateForm
from .serializers import UserSerializer


@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def create_user(request: Request) -> JsonResponse:
    try:
        body = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        return JsonResponse({"errors": ["Malformed request"]}, status=400)

    form = UserCreateForm(body)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors}, status=422)

    user = User.objects.create_user(
        form.cleaned_data["username"], form.cleaned_data["email"], form.cleaned_data["password"]
    )
    user.first_name = form.cleaned_data["first_name"]
    user.last_name = form.cleaned_data["last_name"]
    user.save()

    serializer = UserSerializer(user)

    return JsonResponse(serializer.data)


@api_view(["GET"])
@permission_classes((permissions.AllowAny,))
def get_user(request: Request, id: int) -> JsonResponse:
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse({"errors": ["User not found"]}, status=404)

    serializer = UserSerializer(user)
    return JsonResponse(serializer.data)
