from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from .models import Task
from rest_framework.permissions import IsAuthenticated


# Create your views here.


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)
