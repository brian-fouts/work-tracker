from django.urls import path, re_path

from . import views

urlpatterns = [
    # path("<int:id>/", views.project_actions, name="project"),
    re_path(
        "^(?P<id>.+)/members/$", views.ProjectMemberList.as_view(), name="get-project-members"
    ),
    path("<int:id>/join/", views.join_project, name="join-project"),
    path("<int:id>/leave/", views.leave_project, name="leave-project"),
    path("", views.ProjectViewSet.as_view(), name="project-actions"),
]
