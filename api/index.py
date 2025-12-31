import os
from django.conf import settings
from django.http import HttpResponse
from django.core.handlers.wsgi import WSGIHandler

# Configure Django manually
if not settings.configured:
    settings.configure(
        DEBUG=False,
        SECRET_KEY="vercel-secret-key",
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
        MIDDLEWARE=[],
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
        ],
    )

# URL config
from django.urls import path

def home(request):
    return HttpResponse("✅ Django serverless function is working on Vercel!")

urlpatterns = [
    path("", home),
]

# WSGI application
application = WSGIHandler()
