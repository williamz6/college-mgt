from . import views
from django.urls import path
from users.views import TeacherSignUpForm, StudentSignUpForm

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginUser, name='login'),
    path('register-student/', StudentSignUpForm.as_view(), name='register-student'),
    path('register-teacher/', TeacherSignUpForm.as_view(), name='register-teacher'),
    path('teacher/<slug:teacher_id>/<int:choice>/classes/', views.teacher_class, name='teacher_class'),
    path('teacher/<int:assign_id>/classDates/', views.teacherClass_date, name='teacherClass_date'),
    path('teacher/<int:att_id>/attendance/', views.teacher_attendance, name='teacher_attendance'),
    path('teacher/<int:attclass_id>/attendance/edit', views.edit_attendance, name='edit-attendance'),
    path('teacher/<int:attclass_id>/attendance/confirm', views.confirm_attendance, name='confirm'),
    path('teacher/<int:assign_id>/extra_class/', views.teacher_extra_class, name='extra_class'),
    path('teacher/<slug:assign_id>/extra_class/confirm/', views.e_confirm, name='e_confirm'),
    path('teacher/<int:assign_id>/students/attendance/', views.teacher_student, name='teacher_student'),    
    path('teacher/<str:stud_id>/<slug:course_id>/attendance/', views.teacher_attendance_detail, name='teacher_attendance_detail'),
    path('teacher/<int:att_id>/change_attendance/', views.change_att, name='change_att'),
    path('teacher/<int:assign_id>/marks_list/', views.teacher_marks_list, name='teacher_marks_list'),
    
]
