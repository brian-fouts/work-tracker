from django.urls import path, re_path

from . import views

urlpatterns = [
    path("<slug:id>/", views.get_user, name="get_user"),
    path("", views.create_user, name="create_user"),
]
