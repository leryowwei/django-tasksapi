from rest_framework import permissions, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Task
from .serializers import CategorySerializer, TaskSerializer


class CategoriesApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        """List all the categories for the given requested user."""
        categories = Category.objects.filter(user=request.user.id)
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """Add a category for the given requested user."""
        category_data = {
            "category": request.data.get("category"),
            "user": request.user.id,
        }
        category_serializer = CategorySerializer(data=category_data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data, status=status.HTTP_201_CREATED)
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

        # get category object first. If does not exist, create it via category POST
        category = Category.objects.filter(
            category=request.data.get("category"), user=user_id
        )
        if not category:
            category_view = CategoriesApiView()
            response = category_view.post(request=request)
            if response.status_code != status.HTTP_201_CREATED:
                return response
            category = Category.objects.filter(
                category=request.data.get("category"), user=user_id
            )

        # create task now
        data = {
            "task": request.data.get("task"),
            "category": category.first().pk,
            "priority": request.data.get("priority"),
            "status": request.data.get("status"),
            "user": user_id,
        }
        task_serializer = TaskSerializer(data=data)
        if task_serializer.is_valid():
            task_serializer.save()
            return Response(task_serializer.data, status=status.HTTP_201_CREATED)
        return Response(task_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
