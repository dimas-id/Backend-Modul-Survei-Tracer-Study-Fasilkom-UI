"""
WSGI config for atlas project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

if os.environ.get('PRODUCTION') == 'production':
  WSGIAPP=os.environ.get('HOST_PATH')
  sys.path.append(WSGIAPP)

os.environ['DJANGO_SETTINGS_MODULE'] = 'atlas.settings'

application = get_wsgi_application()
