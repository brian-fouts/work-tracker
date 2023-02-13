"""worktracker URL Configuration"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

import project.views

router = routers.SimpleRouter()
router.register(r"projects", project.views.ProjectViewSet)

urlpatterns = [
    path("users/", include("user.urls")),
    path("work/", include("work.urls")),
    path("admin/", admin.site.urls),
    path("token/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
]

urlpatterns += router.urls
