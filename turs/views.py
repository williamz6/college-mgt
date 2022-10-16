from ast import Not
from django.urls import reverse
from http.client import HTTPResponse

from multiprocessing import context
import re
from time import timezone
from django.shortcuts import get_object_or_404, render, redirect, HttpResponseRedirect
from .models import Assign, Attendance, AttendanceClass, Student, Teacher
from courses.models import Dept, College
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm,TeacherSignUpForm, StudentSignUpForm
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.utils import timezone
User = get_user_model()
# home page
def index(request):      
    teachers = Teacher.objects.all()
    students = Student.objects.all()
   
  


    context = {
        'teachers': teachers,
        'students': students
    }  

    return render(request, 'users/index.html', context)

#login
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == "POST":
        username = request.POST['username'].lower()
        password = request.POST['password']
        
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back {username}!")
            return redirect('profile')
        else:
            messages.error(request, 'Username or Password is incorrect')
    return render(request, 'users/login.html')

# register teacher 
class TeacherSignUpForm(CreateView):
    model = User
    form_class = TeacherSignUpForm
    template_name = 'users/register_teacher.html'
    
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        context['page'] = 'register-teacher'
        context['user_type'] = 'teacher'
        return context
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')
# register student
class StudentSignUpForm(CreateView):
    model= User
    form_class = StudentSignUpForm
    template_name = 'users/register_student.html'
    
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        
        context['page'] = 'register-student'
        context['user_type'] = 'student'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

def profile(request):
    profile = request.user.teacher
     
    context={
        'teacher_obj': profile,
    }
    return render(request, 'users/profile.html', context)

def teacher_class(request, teacher_id, choice):
    teacher_obj = get_object_or_404(Teacher, staff_no=teacher_id)
    context={
        'teacher_obj': teacher_obj,
        'choice': choice
    }
    return render(request, 'users/teacher_class.html', context)

def teacherClass_date(request, assign_id):
    now = timezone.now()
    ass = get_object_or_404(Assign, id=assign_id)
    attendance_list = ass.attendanceclass_set.filter(date__lte=now).order_by('-date')
   
    context={
        'attendance_list': attendance_list,
        'ass':ass
    }
    return render(request, 'users/teacherClass_date.html', context)

def teacher_attendance(request, att_id):
    attendanceclass = get_object_or_404(AttendanceClass, id=att_id)
    ass = attendanceclass.assign
    attendance_c = ass.class_id
    context={
        'attendanceclass':attendanceclass,
        'ass':ass,
        'attendance_c':attendance_c
    }
    return render(request, 'users/teacher_attendance.html', context)

def confirm_attendance(request, attclass_id):
    att_class = get_object_or_404(AttendanceClass, id = attclass_id)
    assign_obj = att_class.assign
    course_obj = assign_obj.course
    class_id = assign_obj.class_id

    for i, student in enumerate(class_id.student_set.all()):
        status = request.POST[student.SID]
        if status == 'present':
            status = 'True'
        else:
            status = 'False'
        if att_class.status == 1:
            try:
                a = Attendance.objects.get(course=course_obj, student=student, attendanceclass=att_class, date=att_class.date)
                a.status= status
                a.save()
            except Attendance.DoesNotExist:
                a=Attendance(course=course_obj, student=student, attendanceclass=att_class, date=att_class.date, status=status)
                a.save()
        else:
            a=Attendance(course=course_obj, student=student, attendanceclass=att_class, date=att_class.date, status=status)
            a.save()
            att_class.status = 1
            att_class.save()
    return HttpResponseRedirect(reverse('teacherClass_date', args=(assign_obj.id,)))

def edit_attendance(request, attclass_id):
    att_class =  get_object_or_404(AttendanceClass, id=attclass_id)
    course_obj = att_class.assign.course
    att_list = Attendance.objects.filter(attendanceclass=att_class, course=course_obj)
    context={
        'att_class': att_class,
        'att_list': att_list,
    }
    return render(request, 'users/edit_attendance.html', context)