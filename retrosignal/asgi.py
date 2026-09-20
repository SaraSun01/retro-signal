"""ASGI config for RetroSignal."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "retrosignal.settings")
application = get_asgi_application()
