"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
# backend/asgi.py
import os

def application():
  from django.core.asgi import get_asgi_application
  # Replace 'myproject' with your project name
  os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
  application = get_asgi_application()
  return application