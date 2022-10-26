"""
WSGI config for talentshow project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

from pathlib import Path
import os

from django.core.wsgi import get_wsgi_application
import dotenv


dotenv.read_dotenv(Path(__file__).resolve().parent.parent / '.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talentshow.settings')

application = get_wsgi_application()
