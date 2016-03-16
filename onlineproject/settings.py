"""
Django settings for onlineproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

ADMINS = ( 
    # ('Your Name', 'your_email@example.com'), 
) 
 
 
MANAGERS = ADMINS 

if 'SERVER_SOFTWARE' in os.environ:
    from sae.const import (MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASS, MYSQL_DB)
else:   

    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_USER = 'zqy_lb'
    MYSQL_PASS = 'passlb'
    MYSQL_DB   = 'online'

    from sae._restful_mysql import monkey
    monkey.patch()

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'NAME':     MYSQL_DB,
        'USER':     MYSQL_USER,
        'PASSWORD': MYSQL_PASS,
        'HOST':     MYSQL_HOST,
        'PORT':     MYSQL_PORT,
    }
}
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '463l%^0a5+@$rcrzou%(1ucgm_$sq^r5v)fikf_&om4ye%1kov'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.staticfiles',
    'online',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'onlineproject.urls'

WSGI_APPLICATION = 'onlineproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
'''
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        #'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME':'online',
        'USER':'zqy_lb',
        'PASSWORD':'passlb',
        'HOST':'localhost',
    }
}'''

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

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
STATIC_ROOT = '' 

STATIC_URL = '/static/'

#STATIC_PATH = './static'

#STATIC_ROOT = os.path.join(os.path.dirname(__file__),'static')
STATICFILES_DIR = (
    #os.path.join(os.path.dirname(__file__),'static').replace('\\','/'),  
)
'''
from django.conf import settings

settings.configure(DEBUG=True, TEMPLATE_DEBUG=True,
    TEMPLATE_DIRS=('/home/web-apps/myapp', '/home/web-apps/base'))
'''
TEMPLATE_DIRS={
    os.path.join(os.path.dirname(__file__),'templates').replace('\\','/'), 
}


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
