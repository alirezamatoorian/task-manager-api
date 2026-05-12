from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "title", "description", "created_by", "status", "priority", "created_at", "updated_at",
                  "due_date", "completed_at"]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
