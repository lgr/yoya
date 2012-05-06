#-*- coding: utf-8 -*-

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'yoya_db_name',
        'USER': 'yoya_db_user',
        'PASSWORD': 'yoya_db_pass',
        'HOST': '',
        'PORT': '',
    }
}

SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'socialregistration.contrib.facebook.auth.FacebookAuth',
)

from settings_common import *

INSTALLED_APPS += (
    'socialregistration',
    'socialregistration.contrib.facebook'
)
