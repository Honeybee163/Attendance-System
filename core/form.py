from django import forms
from core.models import ClassRoom
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from core.models import StudentProfile,CollegeStudent,ClassRoom
from django.core.exceptions import ValidationError
from core.services.student_service import create_student_profile


# design classroom form
class ClassRoomForm(forms.ModelForm):
    class Meta:
        model = ClassRoom
        fields = ['name', 'days_of_week', 'start_date', 'end_date']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter classroom name'}),
            'days_of_week': forms.TextInput(attrs={'placeholder': 'Enter days (e.g., 1 for Monday)'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select start date'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Select end date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if end_date < start_date:
                raise ValidationError({
                    'end_date': "End date cannot be earlier than start date."
                })



# registeration form
class CustomUserCreationForm(UserCreationForm):
    roll_number = forms.CharField(max_length=20, required=True, help_text="Enter your roll number")
    secret_code = forms.CharField(max_length=50, required=True, help_text="Enter college provided secret code")

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'roll_number', 'secret_code']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'John_Doe'}),

        }

    def clean(self):
        cleaned_data = super().clean()
        roll_number = cleaned_data.get('roll_number')
        secret_code = cleaned_data.get('secret_code')

        try:
            student = CollegeStudent.objects.get(roll_number=roll_number, secret_code=secret_code)
        except CollegeStudent.DoesNotExist:
            raise forms.ValidationError("Invalid Roll Number or Secret Code.")

        if student.is_registered:
            raise forms.ValidationError("This student is already registered.")

        # Store the CollegeStudent instance for use in save()
        self.student_instance = student

        return cleaned_data

    def save(self, commit=True):
        # Save the User
        user = super().save(commit)

        roll_number = self.cleaned_data['roll_number']

        # Create student profile
        create_student_profile(user, roll_number)

        # Mark CollegeStudent as registered
        student = getattr(self, 'student_instance', None)
        if student:
            student.is_registered = True
            student.save()

        return user
