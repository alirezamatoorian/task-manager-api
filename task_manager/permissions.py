from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Task


# tasks permissions ---------------
class IsCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "DELETE":
            return obj.created_by == request.user
        if request.method in ["PUT", "PATCH"]:
            return obj.created_by == request.user or request.user in obj.assigned_to.all()
        return False


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


# workspace permissions

class OnlyOwnerCanDeleteOrUpdateWorkspace(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user
