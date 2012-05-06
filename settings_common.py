#-*- coding: utf-8 -*-

import os
import sys
import django
gettext = lambda s: s

ADMINS = (
    ('Admin', 'admin@mysite.es'),
)

MANAGERS = ADMINS

EMAIL_HOST = 'yoya.mail.es'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'yoya@mail.es'
EMAIL_HOST_PASSWORD = 'seret_password'
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "YoYa <yoya@mail.es>"
SERVER_EMAIL = 'yoya@mail.es'

TIME_ZONE = 'Europe/Madrid'
LANGUAGE_CODE = 'es-ES'

USE_I18N = True
USE_L10N = True

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'asdjnasjdadsbiu1239e0dwdjjwed9wjde8723423d'

FACEBOOK_APP_ID = 'facebook_id_goes_here'
FACEBOOK_SECRET_KEY = 'facebook_secret_key'
FACEBOOK_REQUEST_PERMISSIONS = ''


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware'
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'apps.sitemanager.context_processors.site_vars'
)

ROOT_URLCONF = 'urls'

DJANGO_ROOT = os.path.dirname(os.path.realpath(django.__file__))
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))

TEMPLATE_DIRS = (
    os.path.join(SITE_ROOT, "templates").replace("\\", "/"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.humanize',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.comments',
    'django.contrib.sitemaps',
    'registration',
    'apps.profiles',
    'apps.sitemanager',
    'apps.storage',
    'apps.publications',
    'apps.spider',
    'apps.invite_friend',
    'django.contrib.admin'
)

ACCOUNT_ACTIVATION_DAYS = 7
FILE_UPLOAD_PERMISSIONS = 0744

STATIC_ROOT = os.path.join(SITE_ROOT, 'site_media')
MEDIA_ROOT = os.path.join(STATIC_ROOT, 'uploads')
PROXY_ROOT = os.path.join(STATIC_ROOT, 'proxy')
STATIC_URL = '/site_media/'
MEDIA_URL = STATIC_URL + 'uploads/'
PROXY_URL = STATIC_URL + 'proxy/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'

AUTH_PROFILE_MODULE = "profiles.Profile"

DATETIME_FORMAT = "Y-m-d H:i:s"
DATE_FORMAT = "Y-m-d"
DATE_FORMAT_NORM = "Y-m-d"
PYDATE_FORMAT = "%Y-%m-%d"

import logging

logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        filename=os.path.join(SITE_ROOT, 'log/django.log'),
        filemode='w',
       )

LANGUAGES = (
        ('es', gettext('Spanish')),
        ('en', gettext('English')),
        ('pl', gettext('Polish'))
)
