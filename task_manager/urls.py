from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

app_name = "task_manager"
router = DefaultRouter()

router.register("tasks", views.TaskViewSet, basename="tasks")

#nested router for comments
task_router = routers.NestedSimpleRouter(router, "tasks", lookup="tasks")
task_router.register("comments", views.CommentViewSet, basename="comments")

urlpatterns = [
    path('', include(router.urls)),
    path('', include(task_router.urls))

]
