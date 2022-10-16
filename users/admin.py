import imp
from unittest import mock
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Attendance, Teacher, Student, StudentCourse, User, Assign, AssignTime, AttendanceClass, Marks, AttendanceRange
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from django.urls import path
from courses.models import Course

days = {
    'Monday' : 1,
    'Tuesday' : 2,
    'Wednesday' : 3,
    'Thursday' : 4,
    'Friday' : 5,
    'Saturday' : 6,
}
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    list_display= ("id", "name", "created", 'staff_no', 'col')

class StudentAdmin(admin.ModelAdmin):
    list_display= ("SID", "name", 'class_id')

class AssignTimeInline(admin.TabularInline):
    model= AssignTime
    extra= 0

class AssignAdmin(admin.ModelAdmin):
    inlines= [AssignTimeInline]
    list_display=('class_id', 'course', 'teacher')

class MarksInline(admin.TabularInline):
    model = Marks
    extra=0

class StudentCourseAdmin(admin.ModelAdmin):
    inlines=[MarksInline]
    list_display= ['student', 'course', ]


class AttendanceClassAdmin(admin.ModelAdmin):
    list_display= ['assign', 'date', 'status']
    ordering = ['assign', 'date']
    change_list_template = 'admin/attendance/attendance_change_list.html'


    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('reset_attd/', self.reset_attd, name='reset_attd'),
        ]
        return my_urls + urls

    def reset_attd(self, request):

        start_date = datetime.strptime(request.POST['startdate'], '%Y-%m-%d').date()
        end_date = datetime.strptime(request.POST['enddate'], '%Y-%m-%d').date()

        try:
            a = AttendanceRange.objects.all()[:1].get()
            a.start_date = start_date
            a.end_date = end_date
            a.save()
        except AttendanceRange.DoesNotExist:
            a = AttendanceRange(start_date=start_date, end_date=end_date)
            a.save()

        Attendance.objects.all().delete()
        AttendanceClass.objects.all().delete()
        for asst in AssignTime.objects.all():
            for single_date in daterange(start_date, end_date):
                if single_date.isoweekday() == days[asst.day]:
                    try:
                        AttendanceClass.objects.get(date=single_date.strftime("%Y-%m-%d"), assign=asst.assign)
                    except AttendanceClass.DoesNotExist:
                        a = AttendanceClass(date=single_date.strftime("%Y-%m-%d"), assign=asst.assign)
                        a.save()

        self.message_user(request, "Attendance Dates reset successfully!")
        return HttpResponseRedirect("../")



admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Assign, AssignAdmin)
admin.site.register(StudentCourse, StudentCourseAdmin)
admin.site.register(AttendanceClass, AttendanceClassAdmin)