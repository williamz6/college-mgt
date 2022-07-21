import imp
from unittest import mock
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Attendance, Teacher, Student, StudentCourse, User, Assign, AssignTime, AttendanceClass, Marks
from courses.models import Course

days = {
    'Monday' : 1,
    'Tuesday' : 2,
    'Wednesday' : 3,
    'Thursday' : 4,
    'Friday' : 5,
    'Saturday' : 6,
}


# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    list_display= ("id", "name", "created", 'staff_no', 'col')

class StudentAdmin(admin.ModelAdmin):
    list_display= ("id", "name", 'class_id')

class AssignTimeInline(admin.TabularInline):
    model= AssignTime
    extra= 0

class AssignAdmin(admin.ModelAdmin):
    inlines= [AssignTimeInline]
    list_display= ['class_id', 'course', 'teacher']

class MarksInline(admin.TabularInline):
    model = Marks
    extra=0

class StudentCourseAdmin(admin.ModelAdmin):
    inlines=[MarksInline]
    list_display= ['student', 'course']


class AttendanceClassAdmin(admin.ModelAdmin):
    list_display= ['assign', 'date', 'status']



admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Assign, AssignAdmin)
admin.site.register(StudentCourse, StudentCourseAdmin)
admin.site.register(AttendanceClass, AttendanceClassAdmin)