import os
import dj_database_url
from django.conf import settings
from django.http import JsonResponse
from django.urls import path
from django.core.handlers.wsgi import WSGIHandler
import django

# ---------------------------
# Configure Django
# ---------------------------
if not settings.configured:
    settings.configure(
        DEBUG=False,
        SECRET_KEY=os.environ.get("DJANGO_SECRET_KEY", "unsafe-secret"),
        ROOT_URLCONF=__name__,
        ALLOWED_HOSTS=["*"],
        MIDDLEWARE=[
            "django.middleware.common.CommonMiddleware",
        ],
        INSTALLED_APPS=[
            "django.contrib.contenttypes",
            "django.contrib.auth",
        ],
        DATABASES={
            "default": dj_database_url.config(
                default=os.environ.get("DATABASE_URL"),
                ssl_require=True,
            )
        },
    )

# IMPORTANT: initialize Django
django.setup()

# ---------------------------
# Views
# ---------------------------
def home(request):
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1;")
            value = cursor.fetchone()[0]

        return JsonResponse({
            "status": "ok",
            "db": value
        })

    except Exception as e:
        return JsonResponse({
            "status": "error",
            "message": str(e)
        }, status=500)

urlpatterns = [
    path("", home),
]

# ---------------------------
# WSGI application
# ---------------------------
application = WSGIHandler()
