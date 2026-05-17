from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCreatorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.method == "DELETE":
            return obj.created_by == request.user
        if request.method in ["PUT", "PATCH"]:
            return obj.created_by == request.user or request.user in obj.assigned_to.all()
        return False
