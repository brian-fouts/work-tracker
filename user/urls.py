from django.urls import path

from . import views

urlpatterns = [
    path("<int:id>/", views.get_user, name="get-user"),
    path("", views.create_user, name="create-user"),
]
