import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_production'

sys.path.append('/deployment_directory')
sys.path.append('/deployment_directory/lib')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
