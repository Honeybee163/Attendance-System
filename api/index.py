import os

from django.core.wsgi import get_wsgi_application


# Ensure the correct settings module is used on Vercel
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ATTENDANCE.settings")

# Best-effort: create DB tables on cold start for SQLite deployments.
# This keeps demo deployments working without a separate "migrate" step.
if os.getenv("VERCEL") == "1":
    try:
        from django.core.management import call_command

        call_command("migrate", interactive=False, run_syncdb=True, verbosity=0)
    except Exception:
        # If migration fails, Django will surface the real error in logs.
        pass

# Vercel's Python runtime will look for a WSGI callable named `app`
app = get_wsgi_application()

