from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Task, WorkSpace, WorkSpaceMembership




# workspace permissions

class OnlyOwnerCanDeleteOrUpdateWorkspace(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user


# membership permissions

class IsWorkspaceOwnerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        workspaces_id = view.kwargs.get("workspaces_pk")
        workspace = get_object_or_404(WorkSpace, id=workspaces_id)
        try:
            membership = WorkSpaceMembership.objects.get(workspace=workspace, user=request.user)
        except WorkSpaceMembership.DoesNotExist:
            return False
        if request.method in SAFE_METHODS:
            return True
        return (membership.role == WorkSpaceMembership.RoleChoices.OWNER
                or membership.role == WorkSpaceMembership.RoleChoices.ADMIN)

# tasks permissions ---------------
class IsWorkspaceMemberAndTaskPermission(BasePermission):
    def has_permission(self, request, view):
        workspaces_id = view.kwargs.get("workspaces_pk")
        workspace = get_object_or_404(WorkSpace, id=workspaces_id)
        return WorkSpaceMembership.objects.filter(workspace=workspace,user=request.user).exists()

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "DELETE":
            return obj.created_by == request.user
        if request.method in ["PUT", "PATCH"]:
            return obj.created_by == request.user or request.user in obj.assigned_to.all()
        return False


# permission for comments

class IsTaskCreatorOrAssignee(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        task = view.get_task()
        if task.created_by == request.user or request.user in task.assigned_to.all():
            return True
        return False


class OnlyAuthorCanDeleteOrUpdateComment(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return obj.author == request.user
        return True

