from django.contrib.auth.models import User
from django.db import models


class LowerCaseField(models.CharField):
    """Ensure valid values will always be using just lowercase."""

    def get_prep_value(self, value: str | None) -> str | None:
        value = super().get_prep_value(value)
        return value if value is None else value.lower()


class Category(models.Model):
    category = LowerCaseField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["category", "user"], name="user-category")
        ]


class Task(models.Model):
    class Priority(models.IntegerChoices):
        LOW = 1
        MEDIUM = 2
        HIGH = 3

    class Status(models.IntegerChoices):
        NOT_STARTED = 1
        IN_PROGRESS = 2
        REVIEW = 3
        COMPLETED = 4
        CANCELLED = 5

    task = models.CharField(max_length=200, blank=False, null=False)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=False, null=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    priority = models.IntegerField(
        choices=Priority.choices, default=Priority.LOW, blank=False
    )
    status = models.IntegerField(
        choices=Status.choices, default=Status.NOT_STARTED, blank=False
    )
    created = models.DateTimeField(auto_now_add=True, blank=True)
    updated = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.task
