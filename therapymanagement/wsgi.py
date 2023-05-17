"""
WSGI config for therapymanagement project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

import pymysql

pymysql.version_info = (1, 4, 3, "final", 0)
pymysql.install_as_MySQLdb()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapymanagement.settings')

application = get_wsgi_application()

app = application
