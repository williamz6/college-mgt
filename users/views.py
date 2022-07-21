from ast import Not

from multiprocessing import context
from django.shortcuts import render, redirect
from .models import Student, Teacher
from courses.models import Dept, College
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm,TeacherSignUpForm, StudentSignUpForm
from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model
from django.contrib import messages
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
  
    return render(request, 'users/profile.html')

