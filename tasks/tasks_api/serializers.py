from rest_framework import serializers

from .models import Category, Task


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["category", "user", "created", "updated"]


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "task",
            "category",
            "priority",
            "status",
            "user",
            "created",
            "updated",
        ]
