"""
Django settings for parking project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from datetime import datetime, timedelta
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import environ
from corsheaders.defaults import default_headers, default_methods
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])
CORS_ORIGIN_ALLOW_ALL=True
CORS_ALLOW_CREDENTIAL=True
CORS_ALLOWED_ORIGINS=["http://localhost:3000"]
CSRF_COOKIE_HTTPONLY=True
SESSION_COOKIE_HTTPONLY=True
# Application definition

INSTALLED_APPS = [
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "core",
    "sweetify",
    "rest_framework",
    "rest_api",
    "rest_framework_simplejwt",
    "django_filters",
    "django_extensions",
    "django_celery_results",
    "django_celery_beat",
    "import_export",
    "translations",
    "rosetta",
    "corsheaders",
    'drf_yasg',

   
]
# INSTALLED_APPS = [
#     # Django apps
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
    
#     # Third-party apps
#     'modeltranslation',
#     'corsheaders',
#     'rest_framework',
#     'rest_framework_simplejwt',
#     'django_filters',
#     'django_extensions',
#     'django_celery_results',
#     'django_celery_beat',
#     'import_export',
#     'rosetta',
    
#     # Your apps
#     'rest_api',
# ]
#for translation
USE_I18N = True
USE_L10N = True         

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'modeltranslation.middleware.TranslationMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROSETTA_GETTEXT_PROCESSORS = [
    'rosetta.gettext_processors.DjangoGettextProcessor',
]
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True

ROOT_URLCONF = "parking.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR, "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "parking.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    "default": {
        # 'ENGINE': 'django.db.backends.sqlite3',
        # 'NAME': BASE_DIR / 'db.sqlite3',
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": env("DATABASE_NAME"),
        "USER": env("DATABASE_USER"),
        "PASSWORD": env("DATABASE_PASS"),
        "HOST": "localhost",
        # "HOST": "db",  #for docker
        "PORT": "5432",
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': ':memory:',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en"
LANGUAGES = [
    ('en', _('English')),
    ('ne', _('Nepali')),
]

LOCALE_PATHS = [BASE_DIR / 'locale']
TIME_ZONE = "Asia/Kathmandu"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


AUTH_USER_MODEL = "rest_api.CustomUser"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_api.pagination.CustomCursorPagination",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=int(env("ACCESS_TOKEN_LIFETIME"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=int(env("REFRESH_TOKEN_LIFETIME"))),
    "ROTATE_REFRESH_TOKENS": env.bool("ROTATE_REFRESH_TOKENS"),
    "BLACKLIST_AFTER_ROTATION": env.bool("BLACKLIST_AFTER_ROTATION"),
    "ALGORITHM": env("ALGORITHM"),
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUTH_HEADER_TYPES": (env("AUTH_HEADER_TYPES"),),
    "USER_ID_FIELD": env("USER_ID_FIELD"),
    "USER_ID_CLAIM": env("USER_ID_CLAIM"),
    "AUTH_TOKEN_CLASSES": (env("AUTH_TOKEN_CLASSES"),),
    "TOKEN_TYPE_CLAIM": env("TOKEN_TYPE_CLAIM"),
    "JTI_CLAIM": env("JTI_CLAIM"),
}


# celery settings
CELERY_BROKER_URL = "redis://localhost:6379/0"

# set the celery result backend
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# Email setup
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_HOST_USER = "nepalicious.webapp@gmail.com"
EMAIL_HOST_PASSWORD = "qhyj hptr gpda lwgb"
EMAIL_USE_SSL = False
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "nepalicious.webapp@gmail.com"

CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = env("CELERY_RESULT_BACKEND")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = env(
    "CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP", cast=bool
)

# Email settings
EMAIL_BACKEND = env("EMAIL_BACKEND")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env("EMAIL_PORT", cast=int)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
EMAIL_USE_SSL = env("EMAIL_USE_SSL", cast=bool)
EMAIL_USE_TLS = env("EMAIL_USE_TLS", cast=bool)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL")


STATICFILES_DIRS =[
    BASE_DIR / "static"
]

# MEDIA_ROOT = BASE_DIR / 'static/images'
STATIC_ROOT = BASE_DIR / 'staticfiles'

import os

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')