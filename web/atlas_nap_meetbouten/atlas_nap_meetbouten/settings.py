# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import netifaces
from datapunt_generic.generic.database import get_docker_host

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIVA_DIR = os.path.abspath(os.path.join(BASE_DIR, './', 'diva'))

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
DEBUG = False

IP_ADDRESSES = [i.get('addr', '')
                for interface in netifaces.interfaces()
                for i in netifaces.ifaddresses(interface).get(netifaces.AF_INET, [])]

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    '.localdomain',
    '.datalabamsterdam.nl',
    '.datapunt.amsterdam.nl',
    '.amsterdam.nl',
] + IP_ADDRESSES


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django_jenkins',
    'django_extensions',

    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    'corsheaders',

    'atlas_api',
    'datasets.nap',
    'datasets.meetbouten',

    'datapunt_generic.batch',
    'datapunt_generic.generic',
    'datapunt_generic.health',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar', )

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'atlas_nap_meetbouten.urls'

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

WSGI_APPLICATION = 'atlas_nap_meetbouten.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'postgres'),
        'USER': os.getenv('DB_USER', 'docker'),
        'PASSWORD': os.getenv('DB_PASS', 'docker'),
        'HOST': os.getenv('DB_SERVICE', get_docker_host()),
        'PORT': os.getenv('DB_PORT', 5432),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..', 'static'))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
}

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login'

INTERNAL_IPS = ['127.0.0.1']

HEALTH_MODEL = 'nap.Peilmerk'
