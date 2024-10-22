"""
Django settings for bigday project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

import os

import environ
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Initialise environment variables
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# This is a default value and must be changed!
# Rename "localsettings.py.template" to 'localsettings.py' and edit your settings.
# To protect your credentials from leaking to your Git server we added 'localsettings.py' to the gitignore
SECRET_KEY = env('SECRET_KEY', default='u7!-y4k1c6b44q507nr_l+c^12o7ur++cpzyn!$65w^!gum@h%')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Set to "console" for console output of emails or to "smtp" to send real mails
MAIL_BACKEND = "console"

ALLOWED_HOSTS = ["my_website_url", "localhost", '127.0.0.1', "eden-david.onrender.com"]
CSRF_TRUSTED_ORIGINS = [
    "http://example.com",
    'https://127.0.0.1'
]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'guests.apps.GuestsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Add this after SessionMiddleware
    'bigday.language_router.LanguageRouterMiddleware',  # Add your custom middleware
]

ROOT_URLCONF = 'bigday.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join('bigday', 'templates'),
        ],
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

WSGI_APPLICATION = 'bigday.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    # if you want to use the postgres database just uncomment the following lines and comment out the sqlite3 lines
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': env('POSTGRES_DB'),
    #     'USER': env('POSTGRES_USER'),
    #     'PASSWORD': env('POSTGRES_PASSWORD'),
    #     'HOST': env('POSTGRES_SERVER'),
    #     'PORT': env('POSTGRES_PORT'),
    # }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'  # Set the default language

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOCALE_PATHS = [
    f"{BASE_DIR}/locale",  # Specify the path for translation files
]
LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_AGE = None
LANGUAGE_COOKIE_PATH = '/'
LANGUAGE_COOKIE_SECURE = False
LANGUAGE_COOKIE_HTTPONLY = True
LANGUAGE_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 1209600  # 2 weeks, in seconds

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_ROOT = 'static_root'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'bigday', 'static'),
]

# Some default values. Will be overwritten by a localsetting.py (rename 'localsettings.py.template' to 'localsettings.py')
# This is used in a few places where the names of the couple are used
BRIDE_AND_GROOM = 'Bride and Groom'
# the date of your wedding
WEDDING_DATE = 'January 1st, 1969'
# the location of your wedding
WEDDING_LOCATION = 'North Pole, USA'
# This is used in links in save the date / invitations
WEDDING_WEBSITE_URL = 'https://thehappycouple.com'
# base address for all emails
DEFAULT_WEDDING_EMAIL = 'happilyeverafter@example.com'
WEDDING_CC_LIST = []

# Checks, if the 'localsettings.py' is present and set some couple variables
# which are used in a few places.
# Otherwise it will just use some defaults above will persist.

try:
    from .localsettings import *
except ImportError:
    pass

if (MAIL_BACKEND == 'console'):
    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

elif (MAIL_BACKEND == 'smtp'):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # Set email backend to use SMTP


# the address your emails (save the dates/invites/etc.) will come from
DEFAULT_WEDDING_FROM_EMAIL = "davidjacob.cohen55@gmail.com"
# when sending test emails it will use this address
DEFAULT_WEDDING_TEST_EMAIL = DEFAULT_WEDDING_FROM_EMAIL
# the default reply-to of your emails, change, if you want to have your replies somewhere else
DEFAULT_WEDDING_REPLY_EMAIL = DEFAULT_WEDDING_EMAIL
