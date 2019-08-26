import os

from django.core.wsgi import get_wsgi_application

from onlinestore.settings.env import env


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinestore.settings.' + env('ENVIRONMENT'))

application = get_wsgi_application()
