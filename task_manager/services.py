from .models import ActivityLog, Task
from django.db import transaction
from django.utils import timezone
from notifications.services import NotificationService


class TaskService:
    @staticmethod
    def create_task(*,user,workspace,serializer):
        with transaction.atomic():
            task=serializer.save(created_by=user,workspace=workspace)
            assigned_users=serializer.validated_data.get('assigned_to',[])
            for assigned_user in assigned_users:
                if assigned_user != user:
                    NotificationService.create_notification(recipient=assigned_user,title="تسک جدید"
                                                            ,message=f"تسک {task.title}به شما موحل شد " )
            ActivityLog.objects.create(workspace=workspace,
                                   user=user,
                                   target=task,
                                   action=ActivityLog.ActionChoices.CREATE,
                                   description=f"{task.title} created")
        return task
    @staticmethod
    def update_task(*,user,serializer):
        with transaction.atomic():
            instance_task=serializer.instance
            old_status=instance_task.status
            task=serializer.save()
            if old_status != Task.StatusChoices.DONE and task.StatusChoices.DONE:
                task.completed_at=timezone.now()
                task.save(update_fields=['completed_at'])
            elif task.status != Task.StatusChoices.DONE and task.completed_at is not None:
                task.completed_at=None
                task.save(update_fields=['completed_at'])
            ActivityLog.objects.create(user=user
                                       ,workspace=task.workspace,
                                        target=task,
                                        action=ActivityLog.ActionChoices.UPDATE,
                                        description=f"{task.title} updated")
            return task
    @staticmethod
    def delete_task(*,user,task):
        with transaction.atomic():
            ActivityLog.objects.create(workspace=task.workspace,user=user,target=task,
                                       action=ActivityLog.ActionChoices.DELETE,
                                       description=f"Task '{task.title}' deleted")
            task.delete()


class CommentService:
    @staticmethod
    def create_comment(*,user,task,serializer):
        with transaction.atomic():
            comment=serializer.save(author=user,task=task)
            ActivityLog.objects.create(user=user
                                       , workspace=task.workspace,
                                       target=comment,
                                       action=ActivityLog.ActionChoices.CREATE,
                                       description="comment created")
        return comment
    @staticmethod
    def update_comment(*,user,serializer):
        with transaction.atomic():
            comment=serializer.save()
            ActivityLog.objects.create(user=user
                                       ,workspace=comment.task.workspace
                                       ,target=comment
                                       ,action=ActivityLog.ActionChoices.UPDATE
                                       ,description="comment updated")
        return comment
    @staticmethod
    def delete_comment(*,user,comment):
        with transaction.atomic():
            ActivityLog.objects.create(user=user
                                       ,workspace=comment.task.workspace
                                       ,target=comment
                                       ,action=ActivityLog.ActionChoices.DELETE,
                                       description="comment deleted")
            comment.delete()


class TaskAttachmentService:
    @staticmethod
    def create_attachment(*,user,task,serializer):
        with transaction.atomic():
            attachment=serializer.save(uploaded_by=user,task=task)
            ActivityLog.objects.create(user=user,workspace=task.workspace
                                       ,target=attachment
                                       ,action=ActivityLog.ActionChoices.CREATE
                                       ,description=f"{attachment.file.name} created")
            return attachment
    @staticmethod
    def delete_attachment(*,user,attachment):
        with transaction.atomic():
            ActivityLog.objects.create(user=user
                                       ,workspace=attachment.task.workspace
                                       ,target=attachment
                                       ,action=ActivityLog.ActionChoices.DELETE
                                       ,description=f"{attachment.file.name} deleted")
            attachment.delete()
