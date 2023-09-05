from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer


class TasksListApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        """List all the tasks for the given requested user."""
        tasks = Task.objects.filter(user=request.user.id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Add a task for the given requested user."""
        user_id = request.user.id

        # get category object first. If does not exist, create it on the spot
        category = Category.objects.filter(
            category=request.data.get("category"), user=user_id
        )
        if not category:
            category_data = {
                "category": request.data.get("category"),
                "user": request.user.id,
            }
            category_serializer = CategorySerializer(data=category_data)
            if category_serializer.is_valid():
                category_serializer.save()
                category = Category.objects.filter(
                    category=request.data.get("category"), user=user_id
                )
            else:
                return Response(
                    category_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        # create task now
        data = {
            "task": request.data.get("task"),
            "category": category.first().pk,
            "priority": request.data.get("priority"),
            "status": request.data.get("status"),
            "user": request.user.id,
        }
        task_serializer = TaskSerializer(data=data)
        if task_serializer.is_valid():
            task_serializer.save()
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
