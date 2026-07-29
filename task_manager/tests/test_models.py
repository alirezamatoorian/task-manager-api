import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from task_manager.models import TaskAttachment



pytestmark = pytest.mark.django_db





def test_delete_task_attachment_removes_file_from_disk(task,user):
    task_attachment = TaskAttachment.objects.create(task=task,uploaded_by=user
                                                    ,file=SimpleUploadedFile("file.pdf",b"content"))
    file_path=task_attachment.file.path
    assert os.path.exists(file_path)
    task_attachment.delete()
    assert not os.path.exists(file_path)