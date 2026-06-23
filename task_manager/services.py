from .models import ActivityLog
from django.db import transaction


class TaskService:
    @staticmethod
    def create_task(*,user,workspace,serializer):
        with transaction.atomic():
            task=serializer.save(created_by=user,workspace=workspace)
            ActivityLog.objects.create(workspace=workspace,
                                   user=user,
                                   target=task,
                                   action=ActivityLog.ActionChoices.CREATE,
                                   description=f"{task.title} created")
        return task
    def delete_task(*,user,workspace,task):
        with transaction.atomic():
            ActivityLog.objects.create(workspace=workspace,user=user,target=task,
                                       action=ActivityLog.ActionChoices.DELETE,
                                       description=f"Task '{task.title}' deleted")
            task.delete()

