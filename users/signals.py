from .models import Teacher, Student
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        teacher = Teacher.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name,

        )
        subject="Welcome to Devsearch"
        message="We are glad to have you here!"
        
post_save.connect(createProfile, sender=User)  

def updateTeacher(sender, instance, created, **kwargs):
    teacher = instance
    user = teacher.user

    if created == False:
        user.first_name = teacher.name        
        user.email = teacher.email
        user.save()
        print('Profile Updated!')




def updateStudent(sender, instance, created, **kwargs):
    student = instance
    user = student.user

    if created == False:
        user.first_name = student.name
        user.save()
        print('Profile Updated')

post_save.connect(updateTeacher, sender=Teacher)
post_save.connect(updateStudent, sender=Student)
