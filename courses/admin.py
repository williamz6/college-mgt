from django.contrib import admin
from .models import Course, Dept, Class, College
from users.models import Student

# Register your models here.
class CourseInline(admin.TabularInline):
    model= Course
    extra=0

class DeptAdmin(admin.ModelAdmin):
    inlines= [CourseInline]
    list_display = ['id', 'name']

class CourseAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'dept']

class StudentInline(admin.TabularInline):
    model = Student
    extra = 0


class ClassAdmin(admin.ModelAdmin):
    list_display=['id', 'name', 'dept']
    search_fields= ['id', 'dept__name']
    inlines=[StudentInline]

admin.site.register(Dept, DeptAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Class, ClassAdmin)
admin.site.register(College)