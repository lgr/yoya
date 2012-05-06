#-*- coding: utf-8 -*-

DEBUG = False
TEMPLATE_DEBUG = DEBUG
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yoya_db_name',
        'USER': 'yoya_db_user',
        'PASSWORD': 'yoya_db_pass',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

SITE_ID = 2

from settings_common import *

ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
