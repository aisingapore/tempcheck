"""
WSGI config for vishnu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from .settings import DEBUG

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vishnu.settings')

application = get_wsgi_application()
if not DEBUG:
    application = WhiteNoise(application, root="static")
