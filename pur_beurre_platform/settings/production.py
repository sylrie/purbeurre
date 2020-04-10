from . import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import raven

sentry_sdk.init(
    dsn="https://92f1abac630541389667ba3ee12d4ff2@o375878.ingest.sentry.io/5195971",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

SECRET_KEY =  os.environ.get('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['127.0.0.1', '51.77.151.187', 'localhost', 'srpurbeurre.herokuapp.com']

DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': os.environ.get('DB_NAME'),
    'USER': os.environ.get('DB_USER'),
    'PASSWORD': os.environ.get('DB_PASSWORD'),
    'HOST': 'localhost',
    'PORT': '5432',
    }
}

INSTALLED_APPS += [
    'raven.contrib.django.raven_compat',
]

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))	

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')	

# Extra places for collectstatic to find static files.	
STATICFILES_DIRS = (	
    os.path.join(PROJECT_ROOT, 'static'),	
)	

# Simplified static file serving.	
# https://warehouse.python.org/project/whitenoise/	
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'	

db_from_env = dj_database_url.config(conn_max_age=500)	
DATABASES['default'].update(db_from_env)

RAVEN_CONFIG = {
    'dsn': 'https://somethingverylong@sentry.io/216272', # caution replace by your own!!
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