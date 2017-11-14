"""
Django settings for altergot project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# путь до папки media, в общем случае она пуста в начале
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/' # для медии в шаблонах
FILE_UPLOAD_PERMISSIONS = 0o644

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}


THUMBNAIL_FORMAT = 'JPEG'
THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.redis_kvstore.KVStore'
THUMBNAIL_REDIS_HOST = 'localhost' # default
THUMBNAIL_REDIS_PORT = 6379 # default


"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
"""


LOGIN_URL = '/login/'

# пустая папка, сюда будет собирать статику collectstatic
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
#урл для шаблонов
STATIC_URL = '/static/' 

STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "assets"),
	os.path.join(BASE_DIR, "templates/images/"),
	os.path.join(BASE_DIR, "templates/css/"),
]
   

# "Поисковики" статики. Первый ищет статику в STATICFILES_DIRS,
# второй в папках приложений.

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nq*ttx%pl^lw%tmlq$&tz&7qex2#)u(b=a+@re2gchi94sgooc'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

THUMBNAIL_DEBUG = DEBUG

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'sorl.thumbnail',
    'coins',
	'sets',
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

ROOT_URLCONF = 'altergot.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates',],
        'APP_DIRS': True,
        'OPTIONS': {
			'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'altergot.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
	'NAME': 'altergot_db',
	'PASSWORD': 'RfhnsLtymub2Cndjkf',
	'USER': 'altergot_user',
	'CHARSET':'utf8',
	'PORT':'3306',
	'HOST':'localhost',
	'OPTIONS': {
		#	'read_default_file': os.path.join(BASE_DIR,'altergot_mysql.conf'),
			'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE'; SET storage_engine=INNODB",
	}
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'file': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'filename': '/home/www/altergot/logs/debug.log',
		},
    },
	'loggers': {
		#'django': {
		#	'handlers': ['file'],
		#	'level': 'DEBUG',
		#	'propagate': True,
		#},
		'coins': {
			'handlers': ['file'],
			'level': 'DEBUG',
			'propagate': True,
		},
	},
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/"

# secure

SECURE_CONTENT_TYPE_NOSNIFF = True
