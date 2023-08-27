from django.db import models
from django.contrib.auth.models import User


class LowerCaseField(models.CharField):
    """Ensure valid values will always be using just lowercase"""
    def get_prep_value(self, value: str | None) -> str | None:
        value = super().get_prep_value(value)
        return value if value is None else value.lower()


class Category(models.Model):
    category = LowerCaseField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)


class Priority(models.TextChoices):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    

class Tasks(models.Model):
    task = models.CharField(max_length=200, blank=False, null=False)
    completed = models.BooleanField(default=False, blank=False, null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)
