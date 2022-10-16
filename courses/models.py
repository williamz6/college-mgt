from tabnanny import verbose
from unicodedata import name
from django.db import models
from shortuuid.django_fields import ShortUUIDField

class College(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Dept(models.Model):
    name = models.CharField(max_length=50, unique=True)
    college= models.ForeignKey(College, on_delete=models.CASCADE, default=1)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
     # return self.college.name

class Course(models.Model):
    name = models.CharField(max_length=50)
    dept= models.ForeignKey(Dept, on_delete=models.CASCADE, null=True)
    shortname = models.CharField(max_length=20, default= 'CE')
   

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
class Class(models.Model):
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE)
    name= models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'classes'
   
    def __str__(self):
        return f'{self.name}:{self.dept}'
