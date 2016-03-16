"""
WSGI config for onlineproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

'''import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlineproject.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()'''

import os
import sys
root = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(root, '..', 'site-packages'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onlineproject.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()