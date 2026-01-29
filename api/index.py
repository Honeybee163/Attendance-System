import os

from django.core.wsgi import get_wsgi_application


# Ensure the correct settings module is used on Vercel
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ATTENDANCE.settings")

# Vercel's Python runtime will look for a WSGI callable named `app`
app = get_wsgi_application()

