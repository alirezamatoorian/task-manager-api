from celery import shared_task
from .services import NotificationService
from django.contrib.auth import get_user_model

User = get_user_model()



@shared_task
def create_notification_task(recipient_id,title,message):
        NotificationService.create_notification(recipient_id=recipient_id,title=title,message=message)

