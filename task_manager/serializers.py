import os

from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from .models import Task, Comment, WorkSpace, WorkSpaceMembership, TaskAttachment, ActivityLog
from django.utils import timezone
from django.contrib.auth import get_user_model

User = get_user_model()



class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields=["id", "user","workspace","action","description", "created_at"]
        read_only_fields = fields

class AssignedToMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone"]


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "content", "author", "task", "created_at"]
        read_only_fields = ["id", "created_at", "author", "task"]

class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields=["id","file","task","uploaded_by","created_at"]
        read_only_fields=["id","task","uploaded_by","created_at"]

    def validate_file(self, value):
        max_size=5*1024*1024
        if value.size > max_size:
            raise serializers.ValidationError("file size is too big")
        allowed_extensions = {
            ".pdf",
            ".png",
            ".jpg",
            ".jpeg",
        }
        ext = os.path.splitext(value.name)[1].lower()
        if ext not in allowed_extensions:
            raise serializers.ValidationError(
                "Unsupported file type."
            )
        return value


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
    attachments=TaskAttachmentSerializer(many=True,read_only=True)

    class Meta:
        model = Task
        fields = ["id", "title", "description", "created_by", "assigned_to", "assigned_to_ids", "is_assigned_to_me",
                  "status",
                  "priority",
                  "attachments",
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
            for assigned_user in assigned_to:
                if not WorkSpaceMembership.objects.filter(user=assigned_user,workspace=workspace).exists():
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

    # def update(self, instance, validated_data):
    #     old_status = instance.status
    #     task = super().update(instance, validated_data)
    #     if (old_status != task.StatusChoices.DONE
    #             and task.status == task.StatusChoices.DONE):
    #         task.completed_at = timezone.now()
    #     elif task.status != task.StatusChoices.DONE:
    #         task.completed_at = None
    #     task.save()
    #     return task


class WorkSpaceSerializer(serializers.ModelSerializer):
    tasks_count = serializers.IntegerField(read_only=True)
    members = AssignedToMiniSerializer(many=True,required=False,read_only=True)

    class Meta:
        model = WorkSpace
        fields = ["id", "title", "owner", "members", "tasks_count", "created_at", "updated_at"]
        read_only_fields = ["id", "owner", "created_at", "updated_at"]



class WorkSpaceMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkSpaceMembership
        fields = ["id", "workspace", "user", "role", "joined_at"]
        read_only_fields = ["id", "workspace", "joined_at"]

    def validate_role(self, value):
        if value == WorkSpaceMembership.RoleChoices.OWNER:
            raise serializers.ValidationError("cannot assign owner role")
        if self.instance:
            if self.instance.role == WorkSpaceMembership.RoleChoices.OWNER:
                raise serializers.ValidationError("cannot assign owner role")
        return value
