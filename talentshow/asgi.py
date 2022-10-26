"""
ASGI config for talentshow project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
import dotenv


dotenv.read_dotenv(os.path.join(os.path.dirname(__file__)), '.env')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talentshow.settings')

application = get_asgi_application()
