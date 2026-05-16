from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Task(models.Model):
    class StatusChoices(models.TextChoices):
        TODO = "todo", "todo"
        IN_PROGRESS = "in_progress", "in_progress"
        REVIEW = "review", "review"
        DONE = "done", "done"

    class PriorityChoices(models.TextChoices):
        LOW = "low", "low"
        MEDIUM = "medium", "medium"
        HIGH = "high", "high"
        URGENT = "urgent", "urgent"

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=StatusChoices, default=StatusChoices.TODO)
    priority = models.CharField(max_length=20, choices=PriorityChoices, default=PriorityChoices.LOW)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    assigned_to = models.ManyToManyField(User, blank=True, related_name="assigned_tasks")
    due_date = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title
