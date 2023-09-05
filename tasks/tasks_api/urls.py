from django.urls import path

from .views import TasksListApiView

urlpatterns = [path("tasks", TasksListApiView.as_view())]
