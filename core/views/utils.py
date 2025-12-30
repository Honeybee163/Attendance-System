import csv
import os
from django.conf import settings
from django.core.files import File
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from core.models import Attendance



def _generate_csv(classroom, students, attendance_count, classes):
    filename = f"attendance_{classroom.name}_{classroom.end_date}.csv"
    reports_dir = os.path.join(settings.MEDIA_ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)

    path = os.path.join(reports_dir, filename)

    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Roll No", "Student Name", "Classroom", "Present", "Total Classes"])
        for student in students:
            key = f"{student.user.username}_{classroom.name}"
            writer.writerow([
                student.roll_number,
                student.user.username,
                classroom.name,
                attendance_count.get(key, 0),
                classes.get(classroom.name, 0)
            ])

    with open(path, 'rb') as f:
        classroom.report_file.save(filename, File(f), save=True)



def _rollover_attendance(classroom):
    today = timezone.now().date()

    with transaction.atomic():
        Attendance.objects.filter(
            classroom=classroom,
            date__year=today.year,
            date__month=today.month
        ).delete()

        next_month = (today.replace(day=28) + timedelta(days=4))
        records = Attendance.objects.filter(
            classroom=classroom,
            date__month=next_month.month,
            date__year=next_month.year
        )

        for att in records:
            Attendance.objects.create(
                classroom=att.classroom,
                student_profile=att.student_profile,
                attendance=att.attendance,
                date=att.date.replace(month=today.month, year=today.year)
            )
