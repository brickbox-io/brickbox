''' Django settings for brickbox.io project. '''

import os
import sys
import environ

# Environment variables
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

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
    'bb_api',                   # API endpoints and handlers
    'bb_billing',               # Billing and payment processing
    'bb_colo',                  # Colocation management
    'bb_public',                # Public landing pages
    'bb_accounts',              # Account creation and login
    'bb_dashboard',             # Users dashboard
    'bb_data',                  # Collection of data
    'bb_vm',                    # Virtual Machine Rentals
    'bb_webhook',               # Handle incoming and outgoing webhook events

    # Other Apps
    'box',                      # Internal Management API Layer
    'puller',                   # CI/CD Automation Tool
    'tellme',                   # https://github.com/ludrao/django-tellme
    'django_devops',            # Custom DevOps Package

    # Other Apps (3rd Party)
    'pwa',                      # https://github.com/silviolleite/django-pwa
    'compressor',               # https://github.com/django-compressor/django-compressor
    'rest_framework',           # https://www.django-rest-framework.org/#installation
    'rest_framework.authtoken', # https://www.django-rest-framework.org/api-guide/authentication/
    "rest_framework_api_key",   # https://florimondmanca.github.io/djangorestframework-api-key/
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
    'csp.middleware.CSPMiddleware',                         # https://django-csp.readthedocs.io/
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
}


WSGI_APPLICATION = 'brickbox.wsgi.application'

SITE_ID = 1

ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True
# ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# Provider specific settings
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'email',
        ],
        'APP': {
            'client_id': env('SOCIAL_AUTH_GOOGLE_client_id'),
            'secret': env('SOCIAL_AUTH_GOOGLE_secret'),
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
    DB_PASSWORD = env('DEBUG_DB_PASSWORD')
else:
    DB_NAME = 'brickbox-db'
    DB_USER = 'doadmin'
    DB_PASSWORD = env('DB_PASSWORD')

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'brickbox-ci',
            'USER': 'GitHub-Action',
            'PASSWORD': env('TEST_DB_PASSWORD'),
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


SECURE_HSTS_SECONDS = 518400
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# ---------------------------------------------------------------------------- #
#                                 Static Files                                 #
# ---------------------------------------------------------------------------- #
# https://docs.djangoproject.com/en/2.2/howto/static-files/
# https://blog.xoxzo.com/en/2018/08/22/cache-busting-in-django/

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

STATIC_URL = 'static/' # Refrenced via HTML

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

# Handing SCSS https://www.accordbox.com/blog/how-use-scss-sass-your-django-project-python-way/
# COMPRESS_PRECOMPILERS = ( ('text/x-scss', 'django_libsass.SassCompiler'),)

# ----------------------------------- Media ---------------------------------- #
MEDIA_URL = '/media/'

MEDIA_ROOT = '/var/www/brickbox/media/' # Directory/Path where media files will be located


# Login OPTIONS

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
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
    EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD') #Secure Single App Password
else:
    EMAIL_HOST_PASSWORD = env('EMAIL_PASSWORD')

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
PWA_APP_START_URL = '/dashboard/'
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
#                            Content Security Policy                           #
# ---------------------------------------------------------------------------- #
CSP_DEFAULT_SRC =   ("'self'",)

CSP_STYLE_SRC =     (
                        "'self'", "'unsafe-inline'",
                        'fonts.googleapis.com', 'use.fontawesome.com',
                        'accounts.google.com'
                    )

CSP_SCRIPT_SRC =    (
                        "'self'", "'unsafe-inline'",
                        'kit.fontawesome.com', 'fonts.googleapis.com',
                        '*.googletagmanager.com',
                        'accounts.google.com', 'apis.google.com',
                        'js.stripe.com'
                    )

CSP_FONT_SRC =      (
                        "'self'",
                        'fonts.gstatic.com', 'use.fontawesome.com', 'ka-f.fontawesome.com',
                    )

CSP_CONNECT_SRC =   (   "'self'",
                        'ka-f.fontawesome.com',
                        '*.google-analytics.com', '*.analytics.google.com',
                        '*.googletagmanager.com', 'accounts.google.com',
                    )

CSP_IMG_SRC =       (
                        "'self'",
                        "*.googletagmanager.com","*.google-analytics.com"
                    )

CSP_FRAME_SRC = ("'self'", 'js.stripe.com', 'accounts.google.com',)

CSP_MANIFEST_SRC = ("'self'",)

# CSP_INCLUDE_NONCE_IN = ['script-src', 'connect-src']

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
CLIENT_ID_TEST = env('STRIPE_CLIENT_ID_TEST')

STRIPE_SECRET_KEY_TEST = env('STRIPE_SECRET_KEY_TEST')

STRIPE_PUBLISHABLE_KEY_TEST = env('STRIPE_PUBLISHABLE_KEY_TEST')

# ---------------------------- Stripe Credentials ---------------------------- #
CLIENT_ID = env('STRIPE_CLIENT_ID')

STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')

STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')

# ---------------------- DigitalOcean Spaces Credentials --------------------- #
DO_SPACES_KEY = env('DO_SPACES_KEY')
DO_SPACES_SECRET = env('DO_SPACES_SECRET')
