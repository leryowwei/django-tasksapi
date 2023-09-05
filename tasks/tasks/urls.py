"""
URL configuration for tasks project.
"""
from django.contrib import admin
from django.urls import include, path
from tasks_api import urls as tasks_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("", include(tasks_urls)),
]
