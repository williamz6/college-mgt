from ipaddress import v4_int_to_packed
from re import L
from unicodedata import name
from unittest import expectedFailure
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date, datetime, timedelta
from shortuuid.django_fields import ShortUUIDField
from courses.models import Dept, Course, Class, College
from django.dispatch import receiver
from django.db.models.signals import post_save,post_delete
from django.core.exceptions import ValidationError
import datetime
import math
from django.core.validators import MaxValueValidator, MinValueValidator
year = datetime.datetime.now()
year = year.strftime('%y')
col_name = 'TCH'
col_num = '01'
num = 0
time_slots = (
    ('7:30 - 8:30', '7:30 - 8:30'),
    ('8:30 - 9:30', '8:30 - 9:30'),
    ('9:30 - 10:30', '9:30 - 10:30'),
    ('11:00 - 11:50', '11:00 - 11:50'),
    ('11:50 - 12:40', '11:50 - 12:40'),
    ('12:40 - 1:30', '12:40 - 1:30'),
    ('2:30 - 3:30', '2:30 - 3:30'),
    ('3:30 - 4:30', '3:30 - 4:30'),
    ('4:30 - 5:30', '4:30 - 5:30'),
)
DAYS_OF_WEEK=(
    ('Monday', 'Monday'),
    ('Tuesday', 'Tuesday'),
    ('Wednesday', 'Wednesday'),
    ('Thursday', 'Thursday'),
    ('Friday', 'Friday'),
    ('Saturday', 'Saturday'),
)
test_name = (
    ('CAT 1', 'CAT 1'),
    ('CAT 2', 'CAT 2'),
    ('CAT 3', 'CAT 3'),
    ('SEMESTER EXAM', 'SEMESTER EXAM'),
)
def science_college():
    name = Dept.objects.filter(college__name = 'Sciences')
    if name:
        name = 'SCI'
    return name

    
def ids():
    no = Teacher.objects.count()
    if no == None:
        return 1
    else:
        return no + 1
# Create your models here.
SEX_TYPE=(
    ('M', 'Male'),
    ('F', 'Female'),
)
class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)



class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    dept = models.ForeignKey(Dept, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    col = models.CharField(max_length=50, editable=True, default=science_college)
    email = models.EmailField(max_length=200, null=True, blank=True)
    sex = models.CharField(max_length=50, choices=SEX_TYPE)
    DOB=models.DateField(default="1970-01-01")
    created = models.DateTimeField(auto_now_add=True)
    profile_image = models.ImageField(null=True, blank=True)    
    staff_no=models.IntegerField(('STAFF_ID'), default=ids, unique=True, editable=False)
    id = models.CharField(primary_key=True, editable=False, max_length=30)
    

    def __str__(self): 
        return f'{self.name} - {self.dept} '
    
    @property
    def getCollege(self):
        try:
            college = self.dept.college
        except:
            college= ' '
        
        return college
    
    

    def save(self, **kwargs):
        sciences = 'Sciences'
        law = 'Law'
        medicine= 'Medicine'
        engineering = 'Engineering'
        sms= 'Social and Management Sciences'

        if self.getCollege.name == sciences:
            self.col = f'SCI'
        elif self.getCollege.name == law:
            self.col = f'LAW'
        elif self.getCollege.name == medicine:
            self.col = f'MHS'
        elif self.getCollege.name == engineering:
            self.col = f'ENG'
        elif self.getCollege.name == sms:
            self.col = f'SMS'
        

        if not self.id:
            self.id = f'{self.col}/{col_name.upper()}{col_num}/{str(self.staff_no).zfill(3)}'
        super().save(**kwargs)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    class_id=models.ForeignKey(Class, on_delete=models.CASCADE, null=True, blank=True, default=1)
    SID= models.CharField(primary_key='True', max_length=20)
    name = models.CharField(max_length=100)
    sex= models.CharField(max_length=50, choices=SEX_TYPE)
    DOB=models.DateField(default="1998-01-01")
    created = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return self.name
    @property
    def check_status(self):
        if self.user.is_student:
            print('is student')
        else:
            print('not student')
   
class Assign(models.Model):
    class_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    course= models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher= models.ForeignKey(Teacher, on_delete=models.CASCADE)

    class Meta:
        unique_together= [['class_id', 'course', 'teacher']]

    def __str__(self):
        cl= Class.objects.get(id=self.class_id_id)
        cr= Course.objects.get(id=self.course_id)
        te= Teacher.objects.get(id=self.teacher_id)
        return f'{te.name}:{cr.name}:{cl}'

class AssignTime(models.Model):
    assign = models.ForeignKey(Assign, on_delete=models.CASCADE)
    period = models.CharField(max_length=50, choices=time_slots, default='7:30 - 8:30')
    day=models.CharField(max_length=15, choices=DAYS_OF_WEEK)

class AttendanceClass(models.Model):
    assign=models.ForeignKey(Assign, on_delete=models.CASCADE)
    date = models.DateField()
    status= models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'
    def __str__(self):
        return f'{self.assign}'

class Attendance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    attendanceclass = models.ForeignKey(AttendanceClass, on_delete=models.CASCADE)
    date = models.DateField(max_length=30,  default='2022-07-11')
    status= models.BooleanField(default=False)

    def __str__(self):
        return f' {self.student} : {self.course}'

class AttendanceTotal(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('course', 'student'))

    @property
    def attendance_class(self):
        student_obj = Student.objects.get(name = self.student)
        course_obj = Course.objects.get(name = self.course)
        attendance_class = Attendance.objects.filter(course = course_obj, student=student_obj, status='True').count()
        return attendance_class

    @property
    def total_class(self):
        student_obj = Student.objects.get(name = self.student)
        course_obj = Course.objects.get(name = self.course)
        total_class = Attendance.objects.filter(course= course_obj, student=student_obj).count()
        return total_class

    @property
    def attendance(self):
        if self.total_class == 0:
            attendance = 0
        else:
            attendance = round((self.attendance_class / self.total_class) * 100,2)
        return attendance
    
    @property
    def classes_to_attend(self):
        cta = math.ceil((0.75 * (self.total_class - self.attendance_class)) / 0.25)
        if cta < 0 :
            return 0
        return cta
    
class StudentCourse(models.Model):
    student= models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
     
    class Meta:
        verbose_name_plural = 'Marks'
        unique_together = (('student', 'course'))
    def __str__(self):
        student_obj = Student.objects.get(name=self.student)
        course_obj = Course.objects.get(name=self.course)
        return  f'{student_obj.name} : {course_obj.name}'
    # cat means Continuous Assessment Test
    def get_cat(self):
        mark_list= self.marks.set_all()
        m = []
        for mark in mark_list:
            m.append(mark.score)
        cat = math.ceil(sum(m[:3]) / 2)
        return cat

    def get_attendance(self):
        att = AttendanceTotal.objects.get(student=self.student, course=self.course)
        return att.attendance
    
class Marks(models.Model):
    studentcourse = models.ForeignKey(StudentCourse, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=test_name, default='CAT 1')
    score = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])

    unique_together= [['studentcourse', 'name' ]]

    def total_marks(self):
        if self.name == 'Semeseter Exams':
            return 100
        return 20

class MarksClass(models.Model):
    assign=models.ForeignKey(Assign, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=test_name, default='CAT 1')
    status=models.BooleanField(default=False)

    unique_together = [['assign', 'name']]
    def total_marks(self):
        if self.name == 'Semeseter Exams':
            return 100
        return 20

class AttendanceRange(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    
@property
def daterange(start_date, end_date):
    for n in range(int(end_date - start_date).days):
        yield start_date + timedelta(n)

days = {
    'Monday': 1,
    'Tuesday': 2,
    'Wednesday': 3,
    'Thursday': 4,
    'Friday': 5,
    'Saturday': 6,
}

# def create_attendance(sender, instance, created, **kwargs):
#     if created:
#         start_date = AttendanceRange.objects.all()[:1].get().start_date
#         end_date = AttendanceRange.objects.all()[:1].get().end_date
#         for single_date in range(start_date, end_date):
#             if single_date.isoweekday() == days[instance.day]:
#                 try:
#                     AttendanceClass.objects.get(date=single_date.strftime("%Y-%m-%d"), assign = instance.assign)
#                 except AttendanceClass.DoesNotExist:
#                     a = AttendanceClass(date=single_date.strftime("%Y-%m-%d"), assign = instance.assign)
#                     a.save()

# def create_marks(sender, instance, created, **kwargs):
#     if created:
#         if hasattr(instance, 'name'):
#             ass_list = instance.class_id.assign_set.all()
#             for ass in ass_list:
#                 try:
#                     StudentCourse.objects.get(student=instance, course=ass.course)
#                 except StudentCourse.DoesNotExist:
#                     sc=StudentCourse(student=instance, course=ass.course)
#                     sc.save()
#                     sc.marks_set.create(name='CAT 1')
#                     sc.marks_set.create(name='CAT 2')
#                     sc.marks_set.create(name='CAT 3')
#                     sc.marks_set.create(name='SEMESTER EXAM')

#         elif hasattr(instance, 'course'):
#             student_list = instance.class_id.student_set.all()
#             cr = instance.course 
#             for s in student_list:
#                 try:
#                     StudentCourse.objects.get(student=s, course=cr)   
#                 except StudentCourse.DoesNotExist:
#                     sc = StudentCourse(student=s, course=cr)
#                     sc.save()
#                     sc.marks_set.create(name='CAT 1')
#                     sc.marks_set.create(name='CAT 2')
#                     sc.marks_set.create(name='CAT 3')
#                     sc.marks_set.create('SEMESTER EXAM')

# def create_marks_class(sender, instance, created, **kwargs):
#     if created:
#         for name in test_name:
#             try:
#                 MarksClass.objects.get(assign=instance, name=name[0])
#             except MarksClass.DoesNotExist:
#                 m = MarksClass(assign=instance, name=name[0])
#                 m.save()


# def delete_marks(sender, instance, **kwargs):
#     try:
#         student_list=  instance.class_id.student_set.all()
#         StudentCourse.objects.filter(course=instance.course, student__in= student_list).delete()
#     except StudentCourse.DoesNotExist:
#         student_list =  None

# post_save.connect(create_marks, sender=Student)
# post_save.connect(create_marks, sender=Assign)
# post_save.connect(create_marks_class, sender=Assign)
# post_save.connect(create_attendance, sender=AssignTime)
# post_delete.connect(delete_marks, sender=Assign)