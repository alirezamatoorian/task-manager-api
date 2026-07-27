from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from.permissions import IsNotificationRecipient
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.decorators import action
from .models import Notification
from .serializers import NotificationSerializer


# Create your views here.



class NotificationViewSet(ReadOnlyModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated,IsNotificationRecipient]
    http_method_names = ["get","patch"]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['patch'])
    def mark_as_read(self,request,pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save(update_fields=['is_read'])
        return Response({'message': 'notification marked as read'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['patch'])
    def all_marks_as_read(self,request):
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'message': 'all notification marked as read'}, status=status.HTTP_200_OK)

