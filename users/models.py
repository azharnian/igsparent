from django.db import models
from django.contrib.auth.models import User

from PIL import Image

from project.utils import generate_random_filename

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=32, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    is_verified = models.BooleanField(default=False, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='created_by')
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
    
class School(models.Model):
    school_name = models.CharField(max_length=128)
    principle = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'School {self.school_name}'
    
class FrontOffice(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    relation = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'Front Office {self.user.username}'
    
class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    relation = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'Teacher {self.user.username}'
    
class Cohort(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    cohort_name = models.CharField(max_length=128)
    homeroom_teacher = models.CharField(max_length=128)

    def __str__(self) -> str:
        return f'Class / Cohort {self.cohort_name}'

class Student(models.Model):
    cohort_name = models.ForeignKey(Cohort, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_of')
    is_active = models.BooleanField(default=True)
    enrolled_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, related_name='enrolled_by')

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'

class Parent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    child = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='parent_of')
    relation = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    assigned_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='assigned_by')

    def __str__(self) -> str:
        return f'Parent {self.user.first_name} {self.user.last_name} - Child {self.child.user.first_name} {self.child.user.last_name}'