from django.apps import apps
from django.conf import settings
from django.test import SimpleTestCase


class DjangoApplicationSmokeTest(SimpleTestCase):
    def test_django_application_loads(self):
        """Django starts with the RetroSignal settings and app registry."""
        self.assertTrue(settings.configured)
        self.assertTrue(apps.ready)
        self.assertEqual(settings.ROOT_URLCONF, "retrosignal.urls")
