from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("users.urls")),
    path("api/", include("fly.urls", namespace="fly")),
    path("api-auth/", include("rest_framework.urls")),
]
