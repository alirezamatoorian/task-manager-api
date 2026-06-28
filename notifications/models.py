from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User=get_user_model()


class Notification(models.Model):
    recipient=models.ForeignKey(User,on_delete=models.CASCADE,related_name="notifications")
    title=models.CharField(max_length=255)
    message=models.TextField()
    is_read=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return f"notification for {self.recipient}"

