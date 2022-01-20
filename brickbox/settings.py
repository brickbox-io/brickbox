''' Django settings for brickbox.io project. '''

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*k*!&5jkh4%)5$y&g48l9msx+mnzuto5cld*%y92krq*&5uo)c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

ADMINS = [('Justin Merrell', 'merrelljustin@gmail.com'),]

# ------------------------------- Applications ------------------------------- #
INSTALLED_APPS = [
    # Django Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',         # https://docs.djangoproject.com/en/dev/ref/contrib/sites/
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.admindocs', # https://docs.djangoproject.com/en/3.2/ref/contrib/admin/admindocs/

    # brickbox.io Apps
    'django_dash_black',        # https://appseed.us/admin-dashboards/django-dashboard-black
    'bb_api',                   # API endpoints and handlers
    'bb_colo',                  # Colocation management
    'bb_public',                # Public landing pages
    'bb_accounts',              # Account creation and login
    'bb_dashboard',             # Users dashboard
    'bb_data',                  # Collection of data
    'bb_vm',                    # Virtual Machine Rentals
    'bb_webhook',               # Handle incoming and outgoing webhook events

    # Other Apps
    'puller',                   # CI/CD Automation Tool
    'tellme',                   # https://github.com/ludrao/django-tellme
    'django_devops',            # Custom DevOps Package

    # Other Apps (3rd Party)
    'pwa',                      # https://github.com/silviolleite/django-pwa
    'compressor',               # https://github.com/django-compressor/django-compressor
    'rest_framework',           # https://www.django-rest-framework.org/#installation
    'rest_framework.authtoken', # https://www.django-rest-framework.org/api-guide/authentication/
    'oauth2_provider',          # https://django-oauth-toolkit.readthedocs.io/en/latest/install.html
    'django_celery_beat',       # https://github.com/celery/django-celery-beat
    'django_celery_results',    # https://github.com/celery/django-celery-results

    # django-health-check       # https://github.com/KristianOellegaard/django-health-check
    'health_check',                             # required
    'health_check.db',                          # stock Django health checkers
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
    'health_check.contrib.celery',              # requires celery
    'health_check.contrib.celery_ping',         # requires celery
    'health_check.contrib.psutil',              # disk and memory utilization; requires psutil
    # 'health_check.contrib.s3boto3_storage',   # requires boto3 and S3BotoStorage backend
    'health_check.contrib.rabbitmq',            # requires RabbitMQ broker
    # 'health_check.contrib.redis',             # requires Redis broker

    #django-allauth                             # https://django-allauth.readthedocs.io
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

# -------------------------------- Middleware -------------------------------- #
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'brickbox.urls'

# --------------------------------- Templates -------------------------------- #
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------------- Authentication Backends ------------------------- #
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'brickbox.wsgi.application'

SITE_ID = 1

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        # For each OAuth based provider, either add a ``SocialApp``
        # (``socialaccount`` app) containing the required client
        # credentials, or list them here:
        'APP': {
            'client_id': '918414840239-qljh31euklmcem5ec7s72a726r3aofsr.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        }
    }
}

# ---------------------------------------------------------------------------- #
#                            Database Configuration                            #
# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Using DigitalOcean managed database, name provided

if DEBUG:
    DB_NAME = 'debug-brickbox-db'
    DB_USER = 'doadmin'
    DB_PASSWORD = 'dadi8xb2jd71ffx9'
else:
    DB_NAME = 'brickbox-db'
    DB_USER = 'doadmin'
    DB_PASSWORD = 'dadi8xb2jd71ffx9'

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'brickbox-ci',
            'USER': 'GitHub-Action',
            'PASSWORD': '4kXOjCvhh5a3wWV7',
            'HOST': 'brickbox-db-postgresql-do-user-9465762-0.b.db.ondigitalocean.com',
            'PORT': '25060',
            'TEST': {'NAME': 'brickbox-ci'},
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASSWORD,
            'HOST': 'brickbox-db-postgresql-do-user-9465762-0.b.db.ondigitalocean.com',
            'PORT': '25060',
            'TEST': {'NAME': 'brickbox-ci'},
        }
    }


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Eastern'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# ---------------------------------------------------------------------------- #
#                                 Static Files                                 #
# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# https://blog.xoxzo.com/en/2018/08/22/cache-busting-in-django/

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_URL = '/static/' # Refrenced via HTML

STATIC_ROOT = '/var/www/brickbox/static/' # Directory/Path where static files will be located

STATICFILES_DIRS = [
    'bb_api/templates/api_docs_source/build',
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

# ----------------------------------- Media ---------------------------------- #
MEDIA_URL = '/media/'

MEDIA_ROOT = '/var/www/brickbox/media/' # Directory/Path where media files will be located


# Login OPTIONS

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dash/'
LOGOUT_REDIRECT_URL = '/login/'


# ---------------------------------------------------------------------------- #
#                              Email Configuration                             #
# ---------------------------------------------------------------------------- #
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'info@brickbox.io' #Email used for system admin notification purpouses aswell.
DEFAULT_FROM_EMAIL = 'info@brickbox.io'
SERVER_EMAIL = 'info@brickbox.io'
EMAIL_USE_TLS = True

if DEBUG:
    EMAIL_HOST_PASSWORD = 'r0flduqu' #Secure Single App Password
else:
    EMAIL_HOST_PASSWORD = 'r0flduqu'

PASSWORD_RESET_MAIL_FROM_USER = 'info@brickbox.io'    #CRM


# ---------------------------------------------------------------------------- #
#                           Progressive Web App (PWA)                          #
# ---------------------------------------------------------------------------- #
PWA_SERVICE_WORKER_PATH = '/var/www/brickbox/static/pwa/serviceworker.js'

if DEBUG:
    PWA_APP_NAME = 'DEV-brickbox.io'
else:
    PWA_APP_NAME = 'brickbox.io'

PWA_APP_DESCRIPTION = "BUILDING THE FOUNDATION FOR THE ARCHITECTS OF THE FUTURE"
PWA_APP_THEME_COLOR = '#0A0302'
PWA_APP_BACKGROUND_COLOR = '#ffffff'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait'
PWA_APP_START_URL = '/dash/'
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': '/static/images/brickbox160.png',
        'sizes': '160x160'
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/images/brickbox160.png',
        'sizes': '160x160'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/images/brickbox160.png',
        'media':'(device-width:320px) and (device-height:568px) and (-webkit-device-pixel-ratio:2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'

# https://dev.to/rubyflewtoo/upgrading-to-django-3-2-and-fixing-defaultautofield-warnings-518n
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'


# ---------------------------------------------------------------------------- #
#                                    Celery                                    #
# ---------------------------------------------------------------------------- #

CELERY_RESULT_BACKEND = 'django-db'


# ---------------------------------------------------------------------------- #
#                                  VM Settings                                 #
# ---------------------------------------------------------------------------- #

if DEBUG:
    SSH_URL = '134.209.214.111'
else:
    SSH_URL = 'vm.brickbox.io'


# ---------------------------------------------------------------------------- #
#                                   API Keys                                   #
# ---------------------------------------------------------------------------- #

# ----------------------- Stripe Debug/Test Credentials ---------------------- #
CLIENT_ID_TEST = 'ca_KbUZTFe8KqC56Ngh7b4hQUBu0fifyban'

STRIPE_SECRET_KEY_TEST = 'sk_test_51Jb9T1AFJmW5oMdbI6NszFIEwIHNynAa1pHqeUkBRMWAqFUj2XguaLzfFqspuarRB5uqVZPuFkyDb4f5k7WuJ3EE00OqwKdoI4' # pylint: disable=line-too-long

STRIPE_PUBLISHABLE_KEY_TEST = 'pk_test_51Jb9T1AFJmW5oMdbOtpNv8mEKgXZZjdVScjhh1l7wMJ4h2UynWpnIl1tlsmX0Hgt33lE8hyoiKer85GgfHnNjagK00aZMtPtzX' # pylint: disable=line-too-long

# ---------------------------- Stripe Credentials ---------------------------- #
CLIENT_ID = 'ca_KbUZatPIraDbaExd7VA0jkTR6Cb2et76'

STRIPE_SECRET_KEY = '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' # pylint: disable=line-too-long

STRIPE_PUBLISHABLE_KEY = 'pk_live_51Jb9T1AFJmW5oMdb3WcUDAIySK9NYUmd3JrP4rb7NvDupmnM8HfVYdpWHxoNf1HFLcwTAcXGmM23D9VKjfu2vTnz00LAAcLjtx' # pylint: disable=line-too-long

# ---------------------- DigitalOcean Spaces Credentials --------------------- #
DO_SPACES_KEY = 'OU6N4IAG7LSM7B7SZHM7'
DO_SPACES_SECRET = 'Rx93aM8pMDXOh8IKtPFIJv5egFg8/Gbqr1AEtA7XUr0'
