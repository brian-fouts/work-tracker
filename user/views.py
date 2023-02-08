import json

from django.http import JsonResponse
from django.contrib.auth.models import User

from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from .forms import UserCreateForm
from .serializers import UserSerializer


def decode_post_body(request):
    body = request.body
    return json.loads(body)


@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def create_user(request):
    body = decode_post_body(request)
    form = UserCreateForm(body)
    if not form.is_valid():
        return JsonResponse({"errors": form.errors})
        
    user = User.objects.create_user(
        form.cleaned_data["username"],
        form.cleaned_data["email"],
        form.cleaned_data["password"]
    )
    user.first_name = form.cleaned_data["first_name"]
    user.last_name = form.cleaned_data["last_name"]
    user.save()

    serializer = UserSerializer(user)

    return JsonResponse({
        "success": True,
        "user": serializer.data
    })


@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return JsonResponse(
            {"errors": ["User not found"]},
            status=404)
    
    serializer = UserSerializer(user)
    return JsonResponse({
        "user": serializer.data
    })
