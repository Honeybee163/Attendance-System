from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from core.models import StudentProfile
from core.form import CustomUserCreationForm
from core.services.student_service import create_student_profile


# user can login(both teacher and student)
def login_view(request):
    context = {}

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if not user:
            context["error"] = "Invalid credentials"
            return render(request, "login.html", context)

        login(request, user)

        profile = StudentProfile.objects.filter(user=user).first()
        if not profile:
            return HttpResponse("Profile not found")

        # Redirect based on role
        if profile.role == "teacher":
            return redirect("teacher_dashboard")
        else:
            return redirect("student_dashboard")

    return render(request, "login.html", context)


# logout
@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


# user can register
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Form ka save method handle karega:
                                 # - User create
                                 # - StudentProfile create
                                 # - CollegeStudent mark as registered

            return redirect("login")  # Registration ke baad login page

        # Agar form invalid hai, errors ke sath dobara render karo
        return render(request, "register.html", {"user_form": form})

    # GET request
    return render(request, "register.html", {"user_form": CustomUserCreationForm()})
