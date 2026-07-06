from django.contrib import admin
from .models import Notification

# Register your models here.


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["title","is_read","recipient","created_at"]
    list_filter = ["is_read","recipient"]
    ordering = ["-created_at"]
    search_fields = ['recipient__phone']