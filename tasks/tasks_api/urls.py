from django.urls import path

from .views import CategoriesApiView, TasksListApiView

urlpatterns = [
    path("tasks", TasksListApiView.as_view()),
    path("categories", CategoriesApiView.as_view()),
]
