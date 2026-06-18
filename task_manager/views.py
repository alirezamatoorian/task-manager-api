from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer, CommentSerializer, WorkSpaceSerializer, WorkSpaceMembershipSerializer,TaskAttachmentSerializer
from .models import Task, Comment, WorkSpace, WorkSpaceMembership, TaskAttachment,ActivityLog
from rest_framework.permissions import IsAuthenticated
from .permissions import IsWorkspaceMemberAndTaskPermission,OnlyOwnerCanDeleteOrUpdateWorkspace, CommentPermission, \
     IsWorkspaceOwnerOrAdmin,TaskAttachmentPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import TaskPagination
from django.db.models import Q, Count
from rest_framework.exceptions import PermissionDenied


# Create your views here.


class WorkspaceViewSet(ModelViewSet):
    serializer_class = WorkSpaceSerializer
    permission_classes = [IsAuthenticated, OnlyOwnerCanDeleteOrUpdateWorkspace]
    def perform_create(self, serializer):
        workspace = serializer.save(owner=self.request.user)
        WorkSpaceMembership.objects.create(workspace=workspace, user=self.request.user,
                                           role=WorkSpaceMembership.RoleChoices.OWNER)
        return workspace
    def get_queryset(self):
        return (WorkSpace.objects.filter(membership__user=self.request.user).select_related("owner")
                .prefetch_related("members")).annotate(tasks_count=Count("tasks"))


class WorkspaceMembershipViewSet(ModelViewSet):
    serializer_class = WorkSpaceMembershipSerializer
    permission_classes = [IsAuthenticated, IsWorkspaceOwnerOrAdmin]
    def get_workspace(self):
        workspace_id = self.kwargs.get("workspaces_pk")
        return get_object_or_404(WorkSpace, id=workspace_id)
    def perform_create(self, serializer):
        workspace =self.get_workspace()
        return serializer.save(workspace=workspace)

    def perform_destroy(self, instance):
        if instance.role==WorkSpaceMembership.RoleChoices.OWNER:
            raise PermissionDenied("owner can not be deleted")
        instance.delete()

    def get_queryset(self):
        workspace = self.get_workspace()
        return WorkSpaceMembership.objects.filter(workspace=workspace)


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsWorkspaceMemberAndTaskPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "priority"]
    search_fields = ["title"]
    ordering_fields = ["created_at"]
    pagination_class = TaskPagination
    def get_workspace(self):
        workspace_id = self.kwargs.get("workspaces_pk")
        return get_object_or_404(WorkSpace, id=workspace_id)
    def perform_create(self, serializer):
        workspace =self.get_workspace()
        task=serializer.save(created_by=self.request.user, workspace=workspace)
        ActivityLog.objects.create(workspace=workspace, user=self.request.user,action=f"created task",description=f"{task.title} created")
        return task
    def get_queryset(self):
        workspace = self.get_workspace()
        return Task.objects.filter(workspace=workspace).prefetch_related("comments", "assigned_to")


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated,CommentPermission]
    def get_task(self):
        task_id = self.kwargs.get("tasks_pk")
        task = get_object_or_404(Task, id=task_id)
        return task
    def get_queryset(self):
        task = self.get_task()
        return Comment.objects.filter(task=task)
    def perform_create(self, serializer):
        task = self.get_task()
        return serializer.save(author=self.request.user, task=task)



class TaskAttachmentViewSet(ModelViewSet):
    serializer_class = TaskAttachmentSerializer
    permission_classes = [IsAuthenticated,TaskAttachmentPermission]
    http_method_names = ["post","get","delete"]
    def get_task(self):
        task_id = self.kwargs.get("tasks_pk")
        return get_object_or_404(Task, id=task_id)
    def get_queryset(self):
        task =self.get_task()
        return TaskAttachment.objects.filter(task=task).select_related("task__workspace")
    def perform_create(self, serializer):
        task =self.get_task()
        return serializer.save(uploaded_by=self.request.user,task=task)