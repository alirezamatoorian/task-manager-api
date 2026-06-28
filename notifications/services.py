from .models import Notification
from django.db import transaction



class NotificationService:
    @staticmethod
    def create_notification(recipient,title, message):
        with transaction.atomic():
            notification = Notification.objects.create(recipient=recipient,title=title, message=message)
        return notification