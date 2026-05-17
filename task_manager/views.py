from rest_framework.viewsets import ModelViewSet
from .serializers import TaskSerializer
from .models import Task
from rest_framework.permissions import IsAuthenticated
from .permissions import IsCreatorOrReadOnly
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import TaskPagination
from django.db.models import Q


# Create your views here.


class TaskViewSet(ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["status", "priority"]
    search_fields = ["title"]
    ordering_fields = ["created_at"]
    pagination_class = TaskPagination

    def perform_create(self, serializer):
        return serializer.save(created_by=self.request.user)

    def get_queryset(self):
        return (Task.objects.filter(Q(created_by=self.request.user) | Q(assigned_to=self.request.user)).
                prefetch_related("assigned_to"))
