from django.shortcuts import render,get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from.permissions import IsNotificationRecipient
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from .models import Notification
from .serializers import NotificationSerializer


# Create your views here.



class NotificationViewSet(ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated,IsNotificationRecipient]
    http_method_names = ["get","put","patch"]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['patch'])
    def mark_is_read(self):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'message': 'notification marked as read'}, status=status.HTTP_200_OK)

