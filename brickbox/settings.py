"""
Django settings for brickbox project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '*k*!&5jkh4%)5$y&g48l9msx+mnzuto5cld*%y92krq*&5uo)c'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pwa',                  # https://github.com/silviolleite/django-pwa
    'rest_framework',       # https://www.django-rest-framework.org/#installation
    'django_dash_black',    # https://appseed.us/admin-dashboards/django-dashboard-black
    'bb_api',               # API endpoints and handlers
    'bb_public',            # Public landing pages
    'bb_accounts',          # Account creation and login
    'bb_dashboard',         # Users dashboard
    'bb_data',              # Collection of data
]

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

WSGI_APPLICATION = 'brickbox.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# Using DigitalOcean managed database, name provided

if DEBUG:
    DB_NAME = 'debug-brickbox-db'
else:
    DB_NAME = 'brickbox-db'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': 'doadmin',
        'PASSWORD': 'dadi8xb2jd71ffx9',
        'HOST': 'brickbox-db-postgresql-do-user-9465762-0.b.db.ondigitalocean.com',
        'PORT': '25060',
        'test': {'NAME': 'brickbox-ci'},
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/' # Refrenced via HTML

STATIC_ROOT = '/var/www/brickbox/static/' # Directory/Path where static files will be located

# Login OPTIONS

LOGIN_REDIRECT_URL = '/dash/'
LOGOUT_REDIRECT_URL = ''

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
PWA_APP_ORIENTATION = 'any'
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
