from celery import shared_task
from .services import NotificationService




@shared_task
def create_notification_task(recipient_id,title,message):
       return NotificationService.create_notification(recipient_id=recipient_id,title=title,message=message)

