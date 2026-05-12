from django.template.context_processors import request
from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from .models import Task
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return Task.objects.filter(created_by=self.request.user)
