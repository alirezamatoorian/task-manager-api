from django.contrib import admin
from .models import Task, WorkSpace,ActivityLog,Comment


# Register your models here.


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["title", "status", "priority", "created_at"]
    list_filter = ["status", "priority"]
    search_fields = ["title"]
admin.site.register(WorkSpace)
admin.site.register(ActivityLog)
admin.site.register(Comment)
