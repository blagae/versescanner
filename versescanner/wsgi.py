"""
WSGI config for versescanner project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""
import os
import signal
import sys
import time
import traceback

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "versescanner.settings")

try:
    # This application object is used by any WSGI server configured to use this
    # file. This includes Django's development server, if the WSGI_APPLICATION
    # setting points here.
    application = get_wsgi_application()
except Exception:
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
