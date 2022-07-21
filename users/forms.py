import email
from pyexpat import model
from tkinter import Widget
from urllib import request
from django import forms
from django.forms import ModelChoiceField, ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Student, Teacher, SEX_TYPE
from courses.models import Dept, Class
from django.db import transaction
from django.core.exceptions import ValidationError
import datetime
User = get_user_model()


class CustomLoginForm(AuthenticationForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update(
      {'class': 'my-username-class'}
    )
    self.fields['password'].widget.attrs.update(
      {'class': 'my-password-class'}
    )
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

class TeacherSignUpForm(UserCreationForm): 
    name = forms.CharField(widget=forms.widgets.TextInput(attrs={'placeholder':'e.g Jane Doe'}))
    email = forms.EmailField()
    sex = forms.ChoiceField(choices=SEX_TYPE)
    dept = forms.ModelChoiceField(queryset = Dept.objects.all())
    DOB = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class Meta(UserCreationForm.Meta):
        model = User
        fields= ['name', 'username', 'email', 'sex', 'dept', 'DOB']

    def __init__(self, *args, **kwargs):
        super(TeacherSignUpForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
    

    @transaction.atomic
    def save(self):
        
        user = super().save(commit=False)
        user.username = user.username.lower()
        user.first_name = self.cleaned_data.get('name').split()[0]
        user.last_name = self.cleaned_data.get('name').split()[1]
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(
            user=user,
            name=self.cleaned_data.get('name'),
            email=self.cleaned_data.get('email'),
            sex=self.cleaned_data.get('sex'),
            dept=self.cleaned_data.get('dept'),
            DOB=self.cleaned_data.get('DOB'),
            
        )
        return user
    
class StudentSignUpForm(UserCreationForm):
    name = forms.CharField()
    sex = forms.ChoiceField(choices=SEX_TYPE)
    DOB = forms.DateField(initial=datetime.date.today, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
    class_id = forms.ModelChoiceField(queryset=Class.objects.all())
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields= ['name', 'username', 'sex', 'DOB', 'class_id']
           
    def __init__(self, *args, **kwargs):
        super(StudentSignUpForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise ValidationError(f'A User with  {username.upper()} already exists')
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.username = user.username.lower()
        user.first_name = self.cleaned_data.get('name').split()[0]
        user.last_name = self.cleaned_data.get('name').split()[1]
        user.is_student = True
        user.save()
        student = Student.objects.create(
            user=user,
            name=self.cleaned_data.get('name'),
            DOB=self.cleaned_data.get('DOB'),
            class_id=self.cleaned_data.get('class_id')
        )
        return user
