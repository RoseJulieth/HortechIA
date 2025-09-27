"""
WSGI config for hortechia_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys

# Agregar el directorio del proyecto al path
path = '/home/yourusername/hortechia-mvp'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hortechia_project.settings_prod')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()