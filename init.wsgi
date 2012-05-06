import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings_production'

sys.path.append('/home/yoya/www/apps/yoya')
sys.path.append('/home/yoya/www/apps/yoya/lib')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
