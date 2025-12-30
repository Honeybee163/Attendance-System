from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
# Create your models here.
# a class that decides subject name and days of week
class ClassRoom(models.Model):
    name=models.CharField(max_length=100)
    days_of_week=models.JSONField(default=list)
    start_date=models.DateField()
    end_date=models.DateField()
    report_file = models.FileField(upload_to='reports/', null=True, blank=True)
    report_generated_for = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name
    
    def total_class_days(self):
        """Return number of class days between start_date and end_date for selected weekdays."""
        total_days = 0
        current_date = self.start_date
        while current_date <= self.end_date:
            if current_date.weekday() in self.days_of_week:
                total_days += 1
            current_date += timedelta(days=1)

        return total_days



# a class that save student name roll no and role
class StudentProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    class_rooms = models.ManyToManyField('ClassRoom', blank=True)
    roll_number=models.IntegerField(auto_created=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')
    
    def __str__(self):
        return self.user.username






#class that handles users attendance
class Attendance(models.Model):
    student_profile = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,null=True)
    date = models.DateField()
    attendance = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student_profile', 'classroom', 'date')






# college students (filled by admin)
class CollegeStudent(models.Model):
    roll_number = models.CharField(max_length=20, unique=True)
    secret_code = models.CharField(max_length=50)
    is_registered = models.BooleanField(default=False)

    def __str__(self):
        return self.roll_number