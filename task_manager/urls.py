from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = "task_manager"
router = DefaultRouter()

router.register("tasks", views.TaskViewSet, basename="tasks")

urlpatterns = [
    path('', include(router.urls))

]
