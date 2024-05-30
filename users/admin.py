from django.contrib import admin
from .models import Profile, Parent, School, FrontOffice, Cohort, Student, Teacher

class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'is_verified'
    )
    ordering = ('user',)

class UserParentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'child',
        'relation'
    )
    ordering = ('user',)

class UserSchoolAdmin(admin.ModelAdmin):
    list_display = (
        'school_name',
        'principle'
    )

class UserFrontOfficeAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'school',
        'is_active',
        'relation'
    )

class UserTeacherAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'school',
        'is_active',
        'relation'
    )

class UserCohortAdmin(admin.ModelAdmin):
    list_display = (
        'school',
        'cohort_name',
        'homeroom_teacher'
    )

class UserStudentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'cohort_name',
    )

admin.site.register(Profile, UserProfileAdmin)
admin.site.register(Parent, UserParentAdmin)
admin.site.register(School, UserSchoolAdmin)
admin.site.register(FrontOffice, UserFrontOfficeAdmin)
admin.site.register(Teacher, UserTeacherAdmin)
admin.site.register(Cohort, UserCohortAdmin)
admin.site.register(Student, UserStudentAdmin)
