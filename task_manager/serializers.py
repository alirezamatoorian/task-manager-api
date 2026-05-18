from rest_framework import serializers
from .models import Task, Comment
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()


class AssignedToMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone"]


class TaskSerializer(serializers.ModelSerializer):
    assigned_to = AssignedToMiniSerializer(read_only=True, many=True)
    assigned_to_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False,
        source="assigned_to",
        write_only=True
    )

    class Meta:
        model = Task
        fields = ["id", "title", "description", "created_by", "assigned_to", "assigned_to_ids", "status", "priority",
                  "created_at",
                  "updated_at",
                  "due_date", "completed_at"]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]

    def validate(self, attrs):
        user = self.context["request"].user
        task = self.instance
        if self.instance:
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


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content", "author", "task", "created_at"]
        read_only_fields = ["created_at", "author", "task"]
