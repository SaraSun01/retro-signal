"""WSGI config for RetroSignal."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "retrosignal.settings")
application = get_wsgi_application()
