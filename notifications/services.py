from .models import Notification
from django.contrib.auth import get_user_model
User = get_user_model()



class NotificationService:
    @staticmethod
    def create_notification(recipient_id,title, message):
            return Notification.objects.create(recipient_id=recipient_id,title=title, message=message)

