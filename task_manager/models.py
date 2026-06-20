from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

User = get_user_model()


class WorkSpace(models.Model):
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="workspaces")
    members = models.ManyToManyField(User, through="WorkSpaceMembership", blank=True,related_name="workspaces_member")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class WorkSpaceMembership(models.Model):
    class RoleChoices(models.TextChoices):
        ADMIN = "admin", "admin"
        OWNER = "owner", "owner"
        MEMBER = "member", "member"

    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE,related_name="membership")
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="workspace_membership")
    role = models.CharField(max_length=20, choices=RoleChoices, default=RoleChoices.MEMBER)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["workspace", "user"],
                name="unique_workspace_member"
            )
        ]


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
    workspace = models.ForeignKey(WorkSpace, on_delete=models.CASCADE, related_name="tasks")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    assigned_to = models.ManyToManyField(User, blank=True, related_name="assigned_tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author.phone} for {self.task.title} "



class TaskAttachment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="attachments")
    file=models.FileField(upload_to="tasks/attachments/")
    uploaded_by=models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_attachments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name


class ActivityLog(models.Model):
    class ActionChoices(models.TextChoices):
        CREATE = "create", "create"
        UPDATE = "update", "update"
        DELETE = "delete", "delete"
    workspace=models.ForeignKey(WorkSpace, on_delete=models.CASCADE,related_name="activity_logs")
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="activity_logs")
    action = models.CharField(max_length=20,choices=ActionChoices)
    description=models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    target = GenericForeignKey( "content_type","object_id")
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.workspace.title}-{self.action}"
