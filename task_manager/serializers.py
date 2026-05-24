from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from .models import Task, Comment, WorkSpace
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class AssignedToMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "author", "task", "created_at"]
        read_only_fields = ["id", "created_at", "author", "task"]


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = AssignedToMiniSerializer(read_only=True, many=True)
    assigned_to_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False,
        source="assigned_to",
        write_only=True
    )
    comments = CommentSerializer(many=True, read_only=True)
    is_assigned_to_me = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "title", "description", "created_by", "assigned_to", "assigned_to_ids", "is_assigned_to_me",
                  "status",
                  "priority",
                  "created_at",
                  "updated_at",
                  "due_date", "comments", "completed_at"]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def get_is_assigned_to_me(self, obj):
        user = self.context.get("request").user
        return user in obj.assigned_to.all()

    def validate(self, attrs):
        user = self.context["request"].user
        view = self.context["view"]
        workspace_id = view.kwargs.get("workspaces_pk")
        workspace = get_object_or_404(WorkSpace, id=workspace_id)
        assigned_to = attrs.get("assigned_to")
        if assigned_to:
            workspace_members = workspace.members.all()
            for assigned_user in assigned_to:
                if assigned_user not in workspace_members:
                    raise serializers.ValidationError("assigned user must be members of workspace")
        if self.instance:
            task = self.instance
            if task.created_by == user:
                return attrs
            if user in task.assigned_to.all():
                allowed_fields = {"status"}
                incoming_fields = set(attrs.keys())
                if incoming_fields.issubset(allowed_fields):
                    return attrs
                raise serializers.ValidationError("assign user only can change status")
            raise serializers.ValidationError(
                "You do not have permission to perform this action."
            )
        return attrs

    def update(self, instance, validated_data):
        old_status = instance.status
        task = super().update(instance, validated_data)
        if (old_status != task.StatusChoices.DONE
                and task.status == task.StatusChoices.DONE):
            task.completed_at = timezone.now()
        elif task.status != task.StatusChoices.DONE:
            task.completed_at = None
        task.save()
        return task


class WorkSpaceSerializer(serializers.ModelSerializer):
    task_count = serializers.SerializerMethodField()

    class Meta:
        model = WorkSpace
        fields = ["id", "title", "owner", "members", "task_count", "created_at", "updated_at"]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]

    def get_task_count(self, obj):
        return obj.tasks.count()
