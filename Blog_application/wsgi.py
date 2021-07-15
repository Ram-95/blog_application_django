"""
WSGI config for Blog_application project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


curr_env = os.environ.get('DJANGO_ENV')
if curr_env == 'DEV':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'Blog_application.settings.development'
elif curr_env == 'PROD':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'Blog_application.settings.production'

#os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Blog_application.settings')

application = get_wsgi_application()
