from django.urls import path, re_path
from rest_framework import routers

from . import views

urlpatterns = [
    path("<slug:id>/", views.get_project, name="get_project"),
    re_path(
        "^(?P<id>.+)/members/$", views.ProjectMemberViewSet.as_view(), name="get_project_members"
    ),
    path("<slug:id>/join/", views.join_project, name="join_project"),
    path("<slug:id>/leave/", views.leave_project, name="leave_project"),
    path("", views.create_project, name="create_project"),
]
