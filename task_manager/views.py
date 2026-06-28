from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from .serializers import (TaskSerializer, CommentSerializer, WorkSpaceSerializer, WorkSpaceMembershipSerializer,
                          TaskAttachmentSerializer,ActivityLogSerializer)
from .models import Task, Comment, WorkSpace, WorkSpaceMembership, TaskAttachment,ActivityLog
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWorkspaceMemberAndTaskPermission,OnlyOwnerCanDeleteOrUpdateWorkspace, CommentPermission, \
     IsWorkspaceOwnerOrAdmin,TaskAttachmentPermission,ActivityLogPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import TaskPagination
from django.db.models import Q, Count, Model
from rest_framework.exceptions import PermissionDenied
from .services import TaskService,CommentService,TaskAttachmentService


# Create your views here.

class WorkspaceQueryMixin:
    def get_workspace(self):
        workspace_id = self.kwargs.get("workspaces_pk")
        return get_object_or_404(WorkSpace, id=workspace_id)

class TaskQueryMixin:
    def get_task(self):
        task_id = self.kwargs.get("tasks_pk")
        return get_object_or_404(Task, id=task_id)

class WorkspaceViewSet(ModelViewSet):
    serializer_class = WorkSpaceSerializer
    permission_classes = [IsAuthenticated, OnlyOwnerCanDeleteOrUpdateWorkspace]
    def perform_create(self, serializer):
        workspace = serializer.save(owner=self.request.user)
        WorkSpaceMembership.objects.create(workspace=workspace, user=self.request.user,
                                           role=WorkSpaceMembership.RoleChoices.OWNER)
    def get_queryset(self):
        return (WorkSpace.objects.filter(membership__user=self.request.user).select_related("owner")
                .prefetch_related("members")).annotate(tasks_count=Count("tasks"))


class WorkspaceMembershipViewSet(WorkspaceQueryMixin,ModelViewSet):
    serializer_class = WorkSpaceMembershipSerializer
    permission_classes = [IsAuthenticated, IsWorkspaceOwnerOrAdmin]
    def perform_create(self, serializer):
        workspace =self.get_workspace()
        serializer.save(workspace=workspace)
    def perform_destroy(self, instance):
        if instance.role==WorkSpaceMembership.RoleChoices.OWNER:
            raise PermissionDenied("owner can not be deleted")
        instance.delete()
    def get_queryset(self):
        workspace = self.get_workspace()
        return WorkSpaceMembership.objects.filter(workspace=workspace).select_related("user")


class TaskViewSet(WorkspaceQueryMixin,ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsWorkspaceMemberAndTaskPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "priority"]
    search_fields = ["title"]
    ordering_fields = ["created_at"]
    pagination_class = TaskPagination
    def perform_create(self, serializer):
        workspace =self.get_workspace()
        TaskService.create_task(user=self.request.user,workspace=workspace,serializer=serializer)
    def perform_update(self, serializer):
        TaskService.update_task(user=self.request.user,serializer=serializer)
    def perform_destroy(self, instance):
        TaskService.delete_task(user=self.request.user,task=instance)
    def get_queryset(self):
        workspace = self.get_workspace()
        return Task.objects.filter(workspace=workspace).prefetch_related("comments", "assigned_to","attachments")


class CommentViewSet(TaskQueryMixin,ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,CommentPermission]
    def get_queryset(self):
        task = self.get_task()
        return Comment.objects.filter(task=task)
    def perform_create(self, serializer):
        task = self.get_task()
        CommentService.create_comment(user=self.request.user,task=task,serializer=serializer)
    def perform_update(self, serializer):
        CommentService.update_comment(user=self.request.user,serializer=serializer)
    def perform_destroy(self, instance):
        CommentService.delete_comment(user=self.request.user,comment=instance)


class TaskAttachmentViewSet(TaskQueryMixin,ModelViewSet):
    serializer_class = TaskAttachmentSerializer
    permission_classes = [IsAuthenticated,TaskAttachmentPermission]
    http_method_names = ["post","get","delete"]
    def get_queryset(self):
        task =self.get_task()
        return TaskAttachment.objects.filter(task=task).select_related("task__workspace")
    def perform_create(self, serializer):
        task =self.get_task()
        TaskAttachmentService.create_attachment(user=self.request.user,task=task,serializer=serializer)
    def perform_destroy(self, instance):
        TaskAttachmentService.delete_attachment(user=self.request.user,attachment=instance)

class ActivityLogViewSet(WorkspaceQueryMixin,ReadOnlyModelViewSet):
    serializer_class = ActivityLogSerializer
    permission_classes = [IsAuthenticated,ActivityLogPermission]
    def get_queryset(self):
        workspace=self.get_workspace()
        return ActivityLog.objects.filter(workspace=workspace).select_related("user","workspace")