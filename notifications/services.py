from .models import Notification
from django.contrib.auth import get_user_model
User = get_user_model()



class NotificationService:
    @staticmethod
    def create_notification(recipient_id,title, message):
        try:
            recipient = User.objects.get(id=recipient_id)
            notification = Notification.objects.create(recipient=recipient,title=title, message=message)
            return notification
        except User.DoesNotExist:
            return "user does not exist"