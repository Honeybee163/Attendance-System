from django.contrib import admin
from .models import StudentProfile, ClassRoom, Attendance, CollegeStudent

admin.site.register(StudentProfile)
admin.site.register(ClassRoom)
admin.site.register(Attendance)
admin.site.register(CollegeStudent)
