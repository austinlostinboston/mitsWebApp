"""
Django settings for webapps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
<<<<<<< HEAD
TEST_RUNNER = 'weiss.tests.testUtils.NoDbTestRunner'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
=======

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ConfigParser
>>>>>>> c2fce5f... added protected settings file
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'zs%x@)d08$g(s#qin+92-o=6yqmx^)bc5s-y#t&0xko@noc9ph'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Logging settings
<<<<<<< HEAD
logpath = "log/djangoDebug.log"
=======
logpath = os.path.join(BASE_DIR, 'log/djangoLog')
>>>>>>> c2fce5f... added protected settings file


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'weiss',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'webapps.urls'

WSGI_APPLICATION = 'webapps.wsgi.application'

## Handles login redirecting
# Sends unathenticated user to website/login
LOGIN_URL = '/login'
# Directs user to website after logging in
LOGIN_REDIRECT_URL = '/'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }

<<<<<<< HEAD
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
	'NAME': 'weiss',
        'USER': 'weiss',
        'PASSWORD': 'washington',
        'HOST': 'awb.pc.cs.cmu.edu',
        'PORT': '3306',
=======
## Get information from config file
path = os.path.dirname(os.path.realpath(__file__))
config = ConfigParser.ConfigParser()
config.read(path + "/" + "config.ini")

name = config.get('webapp','name')
user = config.get('webapp','user')
password = config.get('webapp','password')
host = config.get('webapp','host')
port = config.get('webapp','port')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
	'NAME': name,
        'USER': user,
        'PASSWORD': password,
        'HOST': host,
        'PORT': port,
>>>>>>> c2fce5f... added protected settings file
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR,'weiss/static'),)

# logging settings
LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
<<<<<<< HEAD
            'format': '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s'
            },
        'simple': {
            'format': '%(levelname)s %(message)s'
=======
            'format': '[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d}\n<%(levelname)s - %(message)s'
            },
        'simple': {
            'format': '{%(pathname)s:%(lineno)d}\n<%(levelname)s %(message)s'
>>>>>>> c2fce5f... added protected settings file
            },
        },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
            },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': logpath,
            'formatter': 'verbose'
            },
        },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
            },
        'weiss': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
            },
        }
    }

if DEBUG:
    # make all loggers use the console.
    for logger in LOGGING['loggers']:
        LOGGING['loggers'][logger]['handlers'] += ['console']

<<<<<<< HEAD
=======
NOSE_ARGS = ['--nocapture', '--nologcapture',]
# Test runner with no database creation
TEST_RUNNER = 'weiss.tests.testUtils.NoDbTestRunner'
>>>>>>> c2fce5f... added protected settings file
