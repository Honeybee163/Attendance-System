from django.urls import path
from core.views import (
    login_view,
    logout_view,
    register_user,
    create_classroom,
    teacher_dashboard,
    student_dashboard,
    view_monthly_report,
    all_classroom,
    mark_attendance,
    count_present_days,
    student_dashboard,
    monthly_report,
    download_attendance_csv,
    Home,
    Contact,
    About,
    favicon,

)

urlpatterns = [
    
    # home
    path('', Home, name='home'),
    path('contact/', Contact, name='contact'),
    path('about/', About, name='about'),
    # Authentication
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    # Registration
    path('register/', register_user, name='register'),

    # Classroom
    path('classroom/create/', create_classroom, name='create_classroom'),
    path('classroom/view_monthly_report/', view_monthly_report, name='view_monthly_report'),


    # Dashboards
    path('dashboard/teacher/', all_classroom, name='all_classes'),
    path('dashboard/teacher/', teacher_dashboard, name='teacher_dashboard'),
    
    # mark attendance
    path('dashboard/teacher/mark_attendance/',mark_attendance , name='mark_attendance'),
    
    # present days
    path('dashboard/teacher/count_present_days/',count_present_days , name='count_present_days'),
    
    # student dashboard
    path('dashboard/student/',student_dashboard , name='student_dashboard'),
    
    # monthly report
    path('dashboard/monthly_report/',monthly_report , name='monthly_report'),
    
    # download attendance csv
    path('dashboard/monthly_report/<int:classroom_id>/download_attendance_csv/', download_attendance_csv, name='download_attendance_csv'),
    
    path("favicon.ico", favicon),

]
