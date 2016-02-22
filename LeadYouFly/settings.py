# -*- coding: utf-8 -*-

"""
Django settings for LeadYouFly project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-lxgg3^qp92z*2mr33&w)5_st6m-p5qxi=qi4_j6vkte=2u$rg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['lol.fibar.cn']

WEBSITE_SIGN = 'L'

HOST = 'http://lol.fibar.cn/'

SEO_HOST = 'http://lol.fibar.cn'


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'LYFAdmin',
    'LYFSite',
    'DjangoUeditor',
    'weichat',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

PASSWORD_HASHERS = {
    'django.contrib.auth.hashers.MD5PasswordHasher'
}

ROOT_URLCONF = 'LeadYouFly.urls'

WSGI_APPLICATION = 'LeadYouFly.wsgi.application'



# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'fibar',
        'USER': 'postgres',  # Not used with sqlite3.
        'PASSWORD': '123456',  # Not used with sqlite3.
        'HOST': 'localhost',  # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',
    }
}

UEDITOR_SETTINGS = {
    "config": {
        'initialFrameWidth': 1200,
        'initialFrameHeight': 500,
        'minFrameWidth': 800,
    },
    "upload": {
        'imagePathFormat': 'img/%(basename)s_%(datetime)s.%(extname)s',
        'imageUrlPrefix': '/',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
    os.path.join(BASE_DIR, 'templates/LYFAdmin'),
)

CSS_DIR = './static/css/'
UPLOAD_DIR = './static/upload/'
OUTPUT_DIR = './static/output/'
IMG_DIR = './static/img/'
JS_DIR = './static/js/'
FONTS_DIR = './static/fonts/'
STATIC_DIR = './static/'
STATIC_ROOT = './static/'
MEDIA_ROOT = './static/upload/'
MEDIA_URL = './upload/'
MEDIA_TMP = './static/tmp/'

QQ_APP_ID = '101284935'
QQ_APP_KEY = 'dd0afc099033522cbbce0229174df168'
