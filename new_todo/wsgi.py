"""
WSGI config for new_todo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'new_todo.settings')

application = get_wsgi_application()
app = application

# Auto-migrate on Vercel
if os.environ.get('VERCEL'):
    from django.core.management import call_command
    try:
        call_command('migrate', interactive=False)
    except Exception as e:
        print(f"Migration error: {e}")