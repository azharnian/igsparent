from django.contrib import admin
from .models import Profile, Parent, School, FrontOffice, Cohort, Student

admin.site.register(Profile)
admin.site.register(Parent)
admin.site.register(School)
admin.site.register(FrontOffice)
admin.site.register(Cohort)
admin.site.register(Student)