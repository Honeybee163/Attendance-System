import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "core.settings"   # 🔴 yahan confirm project name
)

application = get_wsgi_application()
