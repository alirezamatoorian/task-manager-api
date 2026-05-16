from rest_framework import serializers
from .models import Task
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
