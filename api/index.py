import os
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.http import JsonResponse
from django.urls import path
import dj_database_url

# --------------------
# Django configuration
# --------------------
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
                conn_max_age=600,
                ssl_require=True,
            )
        },
    )

# --------------------
# Test route (DB check)
# --------------------
from django.db import connection

def home(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT 1;")
        row = cursor.fetchone()

    return JsonResponse({
        "message": "Django + Neon + Vercel working ✅",
        "db_test": row[0]
    })

urlpatterns = [
    path("", home),
]

# --------------------
# WSGI app
# --------------------
application = WSGIHandler()
