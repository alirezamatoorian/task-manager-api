from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

app_name = "task_manager"
router = DefaultRouter()

router.register("workspaces", views.WorkspaceViewSet, basename="workspaces")


# nested router for membership
membership_router = routers.NestedSimpleRouter(router, "workspaces", lookup="workspaces")
membership_router.register("members", views.WorkspaceMembershipViewSet, basename="members")

#nested router for tasks
workspace_router = routers.NestedSimpleRouter(router, "workspaces", lookup="workspaces")
workspace_router.register("tasks", views.TaskViewSet, basename="tasks")

#nested router for comments
task_router = routers.NestedSimpleRouter(workspace_router, "tasks", lookup="tasks")
task_router.register("comments", views.CommentViewSet, basename="comments")

urlpatterns = [
    path('', include(router.urls)),
    path('',include(membership_router.urls)),
    path('', include(workspace_router.urls)),
    path('', include(task_router.urls))
]
