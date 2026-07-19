from .models import ActivityLog, Task
from django.db import transaction
from django.utils import timezone
from notifications.tasks import create_notification_task


class TaskService:
    @staticmethod
    def create_task(*, user, workspace, serializer):
        with transaction.atomic():
            task = serializer.save(created_by=user, workspace=workspace)
            assigned_users = serializer.validated_data.get('assigned_to', [])
            for assigned_user in assigned_users:
                if assigned_user != user:
                    transaction.on_commit(
                        lambda u=assigned_user: create_notification_task.delay(recipient_id=u.id, title="تسک جدید"
                                                               , message=f" تسک{task.title}به شما محول شد ")
                    )
            ActivityLog.objects.create(workspace=workspace,
                                       user=user,
                                       target=task,
                                       action=ActivityLog.ActionChoices.CREATE,
                                       description=f" تسک{task.title}ایجاد شد ")
        return task

    @staticmethod
    def update_task(*, user, serializer):
        with transaction.atomic():
            instance_task = serializer.instance
            old_status = instance_task.status
            old_assigned_users = set(instance_task.assigned_to.all())
            task = serializer.save()
            if old_status != Task.StatusChoices.DONE and task.status == Task.StatusChoices.DONE:
                task.completed_at = timezone.now()
                task.save(update_fields=['completed_at'])
            elif task.status != Task.StatusChoices.DONE and task.completed_at is not None:
                task.completed_at = None
                task.save(update_fields=['completed_at'])
            new_assigned_users = set(task.assigned_to.all()) - old_assigned_users
            for assigned_user in new_assigned_users:
                if assigned_user != user:
                    transaction.on_commit(
                        lambda u=assigned_user:create_notification_task.delay(recipient_id=u.id, title="تسک جدید",
                                                   message=f"تسک {task.title}به شما محول شد ")
                    )
            ActivityLog.objects.create(user=user
                                       , workspace=task.workspace,
                                       target=task,
                                       action=ActivityLog.ActionChoices.UPDATE,
                                       description=f" تسک{task.title}آپدیت شد ")
        return task

    @staticmethod
    def delete_task(*, user, task):
        with transaction.atomic():
            ActivityLog.objects.create(workspace=task.workspace, user=user, target=task,
                                       action=ActivityLog.ActionChoices.DELETE,
                                       description=f" تسک{task.title}حذف شد ")
            task.delete()


class CommentService:
    @staticmethod
    def create_comment(*, user, task, serializer):
        with transaction.atomic():
            comment = serializer.save(author=user, task=task)
            recipients = (set(task.assigned_to.all()) | {task.created_by}) - {user}
            for recipient in recipients:
                transaction.on_commit(
                lambda r=recipient:create_notification_task.delay(recipient_id=r.id,
                                               title=f" کامنت جدید در{task.title} ",
                                               message=f"{user.phone} کامنت نوشت "
                                               )
                )
            ActivityLog.objects.create(user=user
                                       , workspace=task.workspace,
                                       target=comment,
                                       action=ActivityLog.ActionChoices.CREATE,
                                       description=f"ایجاد شد {task.title}کامنت در ")
        return comment

    @staticmethod
    def update_comment(*, user, serializer):
        with transaction.atomic():
            comment = serializer.save()
            ActivityLog.objects.create(user=user
                                       , workspace=comment.task.workspace
                                       , target=comment
                                       , action=ActivityLog.ActionChoices.UPDATE
                                       , description=f"کامنت {comment.id} در{comment.task.title} آپدیت شد")
        return comment

    @staticmethod
    def delete_comment(*, user, comment):
        with transaction.atomic():
            ActivityLog.objects.create(user=user
                                       , workspace=comment.task.workspace
                                       , target=comment
                                       , action=ActivityLog.ActionChoices.DELETE,
                                       description=f"comment {comment.id} با متن {comment.content[:30]} حذف شد")
            comment.delete()


class TaskAttachmentService:
    @staticmethod
    def create_attachment(*, user, task, serializer):
        with transaction.atomic():
            attachment = serializer.save(uploaded_by=user, task=task)
            # notify all task members except the uploader
            recipients = (set(task.assigned_to.all()) | {task.created_by}) - {user}
            for recipient in recipients:
                transaction.on_commit(
                    lambda r=recipient:create_notification_task.delay(recipient_id=r.id,
                                               title=f"فایلی در {task.title} آپلود شد ",
                                               message=f"{user.phone} آپلود کرد {attachment.file.name}")
                )
            ActivityLog.objects.create(user=user, workspace=task.workspace
                                       , target=attachment
                                       , action=ActivityLog.ActionChoices.CREATE
                                       , description=f"{attachment.file.name} در {task.title} آپلود شد ")
        return attachment

    @staticmethod
    def delete_attachment(*, user, attachment):
        with transaction.atomic():
            ActivityLog.objects.create(user=user
                                       , workspace=attachment.task.workspace
                                       , target=attachment
                                       , action=ActivityLog.ActionChoices.DELETE
                                       , description=f"{attachment.file.name} حذف شد")
            attachment.delete()
