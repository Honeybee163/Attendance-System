from core.models import StudentProfile
from django.contrib.auth.models import User

def create_student_profile(user: User, roll_number: str):
    """
    Create a StudentProfile for the given user with role 'student'.
    """
    return StudentProfile.objects.create(
        user=user,
        roll_number=roll_number,
        role='student'
    )
