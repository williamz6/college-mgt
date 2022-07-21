from . import views
from django.urls import path
from users.views import TeacherSignUpForm, StudentSignUpForm

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.loginUser, name='login'),
    path('register-student/', StudentSignUpForm.as_view(), name='register-student'),
    path('register-teacher/', TeacherSignUpForm.as_view(), name='register-teacher'),
]