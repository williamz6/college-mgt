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
    
]