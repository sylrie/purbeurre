"""
Django settings for pur_beurre_platform project.
Generated by 'django-admin startproject' using Django 3.0.3.
For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/
For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

from . import *
import os
import raven
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

INSTALLED_APPS += ('django_crontab')
SECRET_KEY =  os.environ.get('SECRET_KEY')
CRONTAB_COMMAND_PREFIX = SECRET_KEY

CRONJOBS = [
    ('*/2 * * * *', '~/www/purbeurreenv/bin/python ~/www/purbeurre/manage.py update_database'),
    #('*/1 * * * *', 'pur_beurre_platform.cron.cron_test'),
    #('*/1 * * * *', '~/www/purbeurre/pur_beurre_platform.cron.cron_test'),
    #('0 2 * * 1', 'django.core.management.call_command', ['update_database']),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_URL = '/staticfiles/'

# Static files settings	
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))	

STATIC_ROOT = os.path.join(PROJECT_ROOT, '../staticfiles')	

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (	
    os.path.join(PROJECT_ROOT, 'staticfiles'),	
)
	
db_from_env = dj_database_url.config(conn_max_age=500)	
DATABASES['default'].update(db_from_env)	


sentry_sdk.init(
    dsn="https://dfed232263a24fa98e78ff10715826a3@o375878.ingest.sentry.io/5198764",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

RAVEN_CONFIG = {
    'dsn': 'https://dfed232263a24fa98e78ff10715826a3@o375878.ingest.sentry.io/5198764', # caution replace by your own!!
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO', # WARNING by default. Change this to capture more than warnings.
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'INFO', # To capture more than ERROR, change to WARNING, INFO, etc.
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}