'''
Django settings for atlas project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
'''

import os
import sys
from datetime import timedelta

import environ
import sentry_sdk
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

from atlas.libs.utils.slug import slugify

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

base = environ.Path(__file__) - 2  # two folders back (/a/b/ - 2 = /)
environ.Env.read_env(env_file=base('.env'))  # reading .env file
env = environ.Env(DEBUG=(bool, False), )  # set default values and casting

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('ATLAS_SECRET_KEY')

# should be generated per consumer service
API_KEY = env('ATLAS_API_KEY').strip()

# SECURITY WARNING: don't run with debug turned on in production!
PRODUCTION = os.environ.get('ATLAS_DJANGO_ENV') == 'production'
TESTING = 'test' in sys.argv
DEBUG = not PRODUCTION

PORT = os.environ.get('ATLAS_PORT')
ROOT_URI = env('ATLAS_ROOT_URI')
HELIOS_URI = env('ATLAS_HELIOS_URI')
HYPERION_URI = env('ATLAS_HYPERION_URI')

if PRODUCTION:
    HTTP = 'https://'
else:
    HTTP = 'http://'

DEPLOYMENT_ROOT_URL = HTTP + ROOT_URI

if PORT:
    DEPLOYMENT_ROOT_URL = DEPLOYMENT_ROOT_URL + f':{PORT}'

TOP_LEVEL_DOMAIN = env('ATLAS_TOP_LEVEL_DOMAIN', default='localhost')
FRONTEND_URL = HTTP + HYPERION_URI

# api key
LINKEDIN_CLIENT_ID = env('ATLAS_LINKEDIN_CLIENT_ID')
LINKEDIN_CLIENT_SECRET = env('ATLAS_LINKEDIN_CLIENT_SECRET')
SENDGRID_API_KEY = env('ATLAS_SENDGRID_API_KEY')
CSUI_USERNAME = env('ATLAS_CSUI_USERNAME')
CSUI_PASSWORD = env('ATLAS_CSUI_PASSWORD')

# Application definition
APPS = [
    'atlas',
    'atlas.apps.account',
    'atlas.apps.experience',
    'atlas.apps.external_auth',
    'atlas.apps.contact',
    'atlas.apps.validator'
]

MODULES = [
    'corsheaders',
    'django_extensions',
    'rest_framework',
    'storages',
    'django_rq',
    'jet.dashboard',
    'jet',
]

INSTALLED_APPS = MODULES + APPS + \
    [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

if PRODUCTION and not TESTING:
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]
else:
    # we use whitenoise for local or dev environment for speed
    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

ROOT_URLCONF = 'atlas.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['atlas/templates/'],
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

WSGI_APPLICATION = 'atlas.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': env('ATLAS_SQL_ENGINE'),
        'NAME': env('ATLAS_DB_NAME'),
        'USER': env('ATLAS_DB_POSTGRES_USER'),
        'PASSWORD': env('ATLAS_DB_PASSWORD'),
        'HOST': env('ATLAS_DB_HOST'),
        'PORT': env('ATLAS_DB_PORT')
    }
}

# Django Rest Framework
APPEND_SLASH = False
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'register': '5/min',
    },
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
}

# django autoslug
AUTOSLUG_SLUGIFY_FUNCTION = slugify

# django-rq
RQ_QUEUES = {
    'default': {
        'HOST': env('ATLAS_REDIS_HOST'),
        'PORT': env('ATLAS_REDIS_PORT'),
        'DB': env('ATLAS_REDIS_DB'),
        'DEFAULT_TIMEOUT': env('ATLAS_REDIS_DEFAULT_TIMEOUT'),
    },
}

SILENCED_SYSTEM_CHECKS = ['rest_framework.W001']

# hosts and cors
SERVICE_IP_ADDRESS = env('ATLAS_SERVICE_IP_ADDRESS') 

ALLOWED_HOSTS = ('localhost', '127.0.0.1', ROOT_URI, SERVICE_IP_ADDRESS)
CORS_ORIGIN_WHITELIST = (HYPERION_URI, TOP_LEVEL_DOMAIN)
CORS_ORIGIN_ALLOW_ALL = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',)
AUTH_USER_MODEL = 'account.User'
AUTH_USER_MODEL_LOOKUP_FIELD = 'email'
ALLOW_NATIVE_REGISTER = True

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': env('ATLAS_JWT_SECRET_KEY'),
    'VERIFYING_KEY': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'id'

LANGUAGES = [
    ('id', _('Indonesia')),
    ('en', _('English')),
]

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'atlas/locale'),
)

TIME_ZONE = 'Asia/Jakarta'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')
MEDIA_URL = '/media/'

DEFAULT_PROFILE_PIC = 'https://alumni-prod.s3-ap-southeast-1.amazonaws.com/img/default-profile-pic.jpeg'

# Storage settings
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# sentry
if PRODUCTION:
    sentry_sdk.init(
        dsn="https://5dfd8af44cfc4a0c9d0906be906a2a4b@sentry.io/1442495",
        integrations=[DjangoIntegration()]
    )

# elasticsearch
ELASTICSEARCH_URL = env('ATLAS_ELASTICSEARCH_URL')
ELASTICSEARCH_INDEX = env('ATLAS_ELASTICSEARCH_INDEX')

# sendgrid
SENDGRID_API_KEY = env('ATLAS_SENDGRID_API_KEY')

# jet
JET_DEFAULT_THEME = 'light-blue'
JET_SIDE_MENU_COMPACT = True
JET_CHANGE_FORM_SIBLING_LINKS = True

PROXIES = {
  'http': 'http://proxy.cs.ui.ac.id:8080',
  'https': 'http://proxy.cs.ui.ac.id:8080',
}
