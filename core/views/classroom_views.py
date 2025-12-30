from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,FileResponse, Http404
from core.form import ClassRoomForm
from django.contrib.auth.decorators import login_required
from core.decorators import role_required
from core.models import StudentProfile,ClassRoom,Attendance
from datetime import date, timedelta
from django.db.models import Count,Sum
import csv,io
from django.utils import timezone
import os
from django.db import transaction
from django.core.files import File
from django.conf import settings



# create a calander from which teacher can select date
@login_required
@role_required('teacher')
def create_classroom(request):
    if request.method == 'POST':
        form = ClassRoomForm(request.POST)
        if form.is_valid():
            classroom = form.save()
            try:
                profile = request.user.studentprofile
                profile.class_rooms.add(classroom)
                profile.save()
            except StudentProfile.DoesNotExist:
                return HttpResponse("Profile not found!")
            return redirect('teacher_dashboard')
        # Form invalid: re-render template with errors
        return render(request, 'create_classroom.html', {'form': form})
    
    return render(request, 'create_classroom.html', {'form': ClassRoomForm()})




# count total classrooms 
@login_required
@role_required('teacher')
def all_classroom(request):
    profile=StudentProfile.objects.get(user=request.user)
    print(profile)
    classrooms = profile.class_rooms.all()
    for c in classrooms:
        c.total_days = c.total_class_days()  # add an attribute dynamically
    return render(request, 'teacher_dashboard.html', {'classrooms': classrooms})








# mark attendance
@login_required
@role_required('teacher')
def mark_attendance(request):
    profile = StudentProfile.objects.get(user=request.user)
    # teacher ki classes
    classrooms = profile.class_rooms.all()
    all_students = StudentProfile.objects.filter(
        role='student'
    ).order_by('roll_number')

    if request.method == 'POST':
        classroom_id = request.POST.get('classroom_id')
        classroom = get_object_or_404(ClassRoom, id=classroom_id)
        present_students = request.POST.getlist('present_students')
        today = date.today()

        for student in all_students:
            Attendance.objects.update_or_create(
                student_profile=student,
                classroom=classroom,
                date=today,
                defaults={
                    'attendance': str(student.id) in present_students
                }
            )

        # Redirect to teacher dashboard after saving
        return redirect('/dashboard/teacher/')  # or use named URL

    return render(
        request,
        'mark_attendance.html',
        {
            'data': all_students,
            'classrooms': classrooms
        }
    )








# count total number of days each student is present
def count_present_days(request):
    all_students = StudentProfile.objects.filter(role='student')
    classrooms = ClassRoom.objects.all()
    for c in classrooms:
        c.total_days = c.total_class_days()
        for student in all_students:
            a=Attendance.objects.filter(student_profile=student)
            student.present_days=a.Count()
    return render(request, 'count_present_days.html', {'data': all_students,'total_days':c.total_days})



   
  
  
  
# view monthly report
@login_required
@role_required('teacher')
def view_monthly_report(request):
    all_students = StudentProfile.objects.filter(role='student')
    profile = StudentProfile.objects.get(user=request.user)
    classrooms = profile.class_rooms.all()
    
    attendance_count = {}
    for student in all_students:
        for classroom in classrooms:
            total_present = Attendance.objects.filter(
                student_profile=student,
                classroom=classroom,
                attendance=1
            ).count()
            key = f"{student.user.username}_{classroom.name}"
            attendance_count[key] = total_present
           
    classes = {}
    for classroom in classrooms:
        total_classes = Attendance.objects.filter(
            classroom=classroom
        ).values('date').distinct().count()
        classes[classroom.name] = total_classes

        # ✅ Generate CSV if end_date has passed and report_file doesn't exist
        if classroom.end_date < date.today() and not classroom.report_file:
            filename = f"attendance_{classroom.name}_{classroom.end_date}.csv"
            reports_dir = os.path.join(settings.MEDIA_ROOT, "reports")
            os.makedirs(reports_dir, exist_ok=True)
            file_path = os.path.join(reports_dir, filename)

            # write CSV
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Roll No", "Student Name", "Classroom", "Present", "Total Classes"])
                for student in all_students:
                    key = f"{student.user.username}_{classroom.name}"
                    writer.writerow([
                        student.roll_number,
                        student.user.username,
                        classroom.name,
                        attendance_count.get(key, 0),
                        classes.get(classroom.name, 0)
                    ])

            # save CSV to report_file field
            with open(file_path, 'rb') as f:
                classroom.report_file.save(filename, File(f), save=True)

    return render(request, 'view_students.html', {
        'all_students': all_students,
        'classrooms': classrooms,
        'attendance_count': attendance_count,
        'classes': classes,
        'today': date.today(),
    })

  



@login_required
@role_required('teacher')
def monthly_report(request):
    all_students = StudentProfile.objects.filter(role='student')
    teacher_profile = StudentProfile.objects.get(user=request.user)
    classrooms = teacher_profile.class_rooms.all()

    attendance_count = {}
    classes = {}

    for classroom in classrooms:
        # total classes for this classroom
        classes[classroom.name] = Attendance.objects.filter(
            classroom=classroom
        ).values('date').distinct().count()

        for student in all_students:
            total_present = Attendance.objects.filter(
                student_profile=student,
                classroom=classroom,
                attendance=1
            ).count()
            key = f"{student.user.username}_{classroom.name}"
            attendance_count[key] = total_present

    context = {
        "all_students": all_students,
        "classrooms": classrooms,
        "attendance_count": attendance_count,
        "classes": classes,
    }

    return render(request, "monthly_report.html", context)








@login_required
@role_required('teacher')
def download_attendance_csv(request, classroom_id):
    classroom = ClassRoom.objects.get(id=classroom_id)
    all_students = StudentProfile.objects.filter(role='student')
    classes_count = Attendance.objects.filter(classroom=classroom).values('date').distinct().count()

    # Use HttpResponse instead of FileResponse for CSV
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="attendance_{classroom.name}.csv"'

    writer = csv.writer(response)
    writer.writerow(["Roll No", "Student Name", "Classroom", "Present", "Total Classes","Percentage"])

    for student in all_students:
        total_present = Attendance.objects.filter(
            classroom=classroom, student_profile=student, attendance=1
        ).count()
        if classes_count > 0:
            percentage = (total_present / classes_count) * 100
        else:
            percentage = 0
        writer.writerow([
            student.roll_number,
            student.user.username,
            classroom.name,
            total_present,
            classes_count,
            f"{percentage:.2f}%" 
        ])


    return response
