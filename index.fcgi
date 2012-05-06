#!/usr/bin/python
import sys
import os

# Add a custom Python path. (optional)
#sys.path.insert(0, "/home/username")

# Switch to the directory of your project.
os.chdir("/home/yoya/www/apps/yoya")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ['DJANGO_SETTINGS_MODULE'] = "yoya.settings"

from django.core.servers.fastcgi import runfastcgi
runfastcgi(method="threaded", daemonize="false")
