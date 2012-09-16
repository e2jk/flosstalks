#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Django settings for flosstalks project.
import os

PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
ROOT_PATH = os.path.realpath("%s/.." % PROJECT_PATH)

try:
    # Determines if we're in a production or development environment
    # Create a file called settings_production.py to indicate that this is PRD
    import settings_production
    # Production settings
    DEBUG = False
    TEMPLATE_DEBUG = DEBUG
    # Use caching in the production environment
    DEACTIVATE_CACHE = False
except ImportError:
    # The development environment does not contain a settings_production.py file
    # Development settings
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    # Do not use caching in the development environment
    DEACTIVATE_CACHE = True

ADMINS = (
    ('Emilien Klein', 'emilien@flosstalks.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(ROOT_PATH, 'data/flosstalks.sqlite'),
    }
}

FIXTURE_DIRS = ("data",)

# Caching setup
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_SECONDS = 864000 # 10 days
if DEACTIVATE_CACHE:
    cache_backend = 'django.core.cache.backends.dummy.DummyCache'
else:
    cache_backend = 'django.core.cache.backends.filebased.FileBasedCache'
CACHES = {
    'default': {
        # Use Filesystem caching for running on a low-memory server
        'BACKEND': cache_backend,
        'LOCATION': '/var/cache/django_cache/flosstalks',
        'TIMEOUT': CACHE_MIDDLEWARE_SECONDS,
        'OPTIONS': {
            'MAX_ENTRIES': 1000
        },
        'CULL_FREQUENCY': 5,
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = None #'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# Valid languages
# New languages should be added here when their translation gets available
LANGUAGES = (
  ('en', 'English'),
  ('fr', 'French'),
  ('ru', 'Russian'),
)

LOCALE_PATHS = (
    os.path.join(ROOT_PATH, 'locale'),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(PROJECT_PATH, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
# The secret key is stored in a file that is not put under version control
# TODO: improve with automatic secret key creation. See:
# http://stackoverflow.com/questions/4664724/distributing-django-projects-with-unique-secret-keys#answer-4674143
from DO_NOT_SHARE import SECRET_KEY as sk
SECRET_KEY = sk

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware', # For caching
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware', # For caching
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'flosstalks.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'flosstalks.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    #"/home/emilien/devel/flosstalks/flosstalks_app/templates"
    os.path.join(PROJECT_PATH, 'templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    "flosstalks_app",
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
