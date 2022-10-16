from django.test import TestCase
# from courses.models import College from
from courses.models import College

from .models import Student

# college= College.objects.all().values('name','id')
# print(college)
# Create your tests here.

# year = input("Enter year: ")
# college = input("Enter college: ")
# col_num = input("col num: ")
# num = 0
# while num < 200:
#     num = num + 1
#     print(f'{year}/{college.upper()}{col_num}/{str(num).zfill(3)}')

@property  
def getStuden(self):
    
    college= self.College_set.all().values('name', 'id')
      
    return college
college= ''
print(f'is {college}')