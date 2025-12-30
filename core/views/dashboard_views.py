# views/dashboard_views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from core.decorators import role_required
from core.models import StudentProfile,Attendance,ClassRoom
import matplotlib.pyplot as plt
from django.db.models import Count
from io import BytesIO
import base64
from matplotlib.ticker import MaxNLocator


# teachers dasboard
@login_required
@role_required('teacher')
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')







# student dashboard
@login_required
@role_required('student')
def student_dashboard(request):
    student_profile = StudentProfile.objects.get(user=request.user)
    attendance = Attendance.objects.filter(student_profile=student_profile)

    total_classes = {}
    present_classes = {}

    for a in attendance:
        subject = a.classroom.name

        total_classes[subject] = total_classes.get(subject, 0) + 1

        if a.attendance == 1:
            present_classes[subject] = present_classes.get(subject, 0) + 1

    # Prepare data for graph
    subjects = list(total_classes.keys())
    total = [total_classes[s] for s in subjects]
    present = [present_classes.get(s, 0) for s in subjects]

    # Create bar chart
    plt.figure(figsize=(8, 5))
    x = range(len(subjects))

    plt.bar(x, total, width=0.4, label='Total Classes', color='#5F6F63')
    plt.bar([i + 0.4 for i in x], present, width=0.4, label='Present', color='#E3E6EB')

    plt.xticks([i + 0.2 for i in x], subjects, rotation=45)
    plt.ylabel("Number of Classes")
    plt.title("Attendance per Subject")
    plt.legend()
    plt.tight_layout()

    # Force y-axis to use integers only
    ax = plt.gca()  # Get current axes
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))

    # Convert plot to image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    plt.close()

    graph = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'student_dashboard.html', {
        'user': student_profile,
        'graph': graph
    })

