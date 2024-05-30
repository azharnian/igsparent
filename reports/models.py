from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from users.models import Student

import os
import uuid
from PIL import Image

from project.utils import generate_random_filename

# Create your models here.
class ReportStatus(models.Model):
    report_status_title = models.CharField(max_length=256)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_status_creators')

    def __str__(self) -> str:
        return f'{self.id}-{self.report_status_title}'

class ReportType(models.Model):
    report_type_title = models.CharField(max_length=256)
    date_created = models.DateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_type_creators')

    def __str__(self) -> str:
        return f'{self.id}-{self.report_type_title}'

class Report(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_students')
    report_type = models.ForeignKey(ReportType, on_delete=models.CASCADE, related_name='report_types')
    report_title = models.CharField(max_length=256)
    report_content = models.TextField()
    image = models.ImageField(default='default.jpg', upload_to='report_pics')
    date_created = models.DateTimeField(default=timezone.now)
    report_status = models.ForeignKey(ReportStatus, on_delete=models.CASCADE, related_name='report_status')
    image_url = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    is_approved = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_creators')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='report_approver', null=True)

    def __str__(self) -> str:
        return f'{self.student.user.first_name}-{self.report_title}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)
