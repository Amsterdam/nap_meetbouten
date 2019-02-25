# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

import os
import sys

from datapunt_generic.generic.database import get_docker_host, in_docker

OVERRIDE_HOST_ENV_VAR = 'DATABASE_HOST_OVERRIDE'
OVERRIDE_PORT_ENV_VAR = 'DATABASE_PORT_OVERRIDE'

OVERRIDE_EL_HOST_VAR = 'ELASTIC_HOST_OVERRIDE'
OVERRIDE_EL_PORT_VAR = 'ELASTIC_PORT_OVERRIDE'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))

DIVA_DIR = '/app/data'

if not os.path.exists(DIVA_DIR):
    DIVA_DIR = os.path.abspath(os.path.join(PROJECT_DIR, 'diva'))
    print("Geen lokale DIVA bestanden gevonden, maak gebruik van testset",
          DIVA_DIR, "\n")


class Location_key:
    local = 'local'
    docker = 'docker'
    override = 'override'


def get_database_key():
    if os.getenv(OVERRIDE_HOST_ENV_VAR) and os.getenv(OVERRIDE_EL_HOST_VAR):
        return Location_key.override
    elif in_docker():
        return Location_key.docker

    return Location_key.local


SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")

DEBUG = SECRET_KEY == 'default-secret'

NO_INTEGRATION_TESTS = True

ALLOWED_HOSTS = ['*']

DATAPUNT_API_URL = os.getenv(
    # note the ending /
    'DATAPUNT_API_URL', 'https://api.data.amsterdam.nl/')

# Application definition

INSTALLED_APPS = (
    'geo_views',
    'datapunt_api',
    'datasets.nap',
    'datasets.meetbouten',
    'nap_commands',

    # legacy stuff? still used?
    'batch',
    'datapunt_generic.generic',
    'datapunt_generic.health',

    'django_filters',
    'django_extensions',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_swagger',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

if DEBUG:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware',)

ROOT_URLCONF = 'nap_meetbouten.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nap_meetbouten.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases


DATABASE_OPTIONS = {
    Location_key.docker: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'nap'),
        'USER': os.getenv('DATABASE_USER', 'nap'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': 'database',
        'PORT': '5432'
    },
    Location_key.local: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'nap'),
        'USER': os.getenv('DATABASE_USER', 'nap'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': get_docker_host(),
        'PORT': '5401'
    },
    Location_key.override: {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DATABASE_NAME', 'nap'),
        'USER': os.getenv('DATABASE_USER', 'nap'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD', 'insecure'),
        'HOST': os.getenv(OVERRIDE_HOST_ENV_VAR),
        'PORT': os.getenv(OVERRIDE_PORT_ENV_VAR, '5432')
    },
}

DATABASES = {
    'default': DATABASE_OPTIONS[get_database_key()]
}


EL_HOST_VAR = os.getenv(OVERRIDE_EL_HOST_VAR)
EL_PORT_VAR = os.getenv(OVERRIDE_EL_PORT_VAR, '9200')


ELASTIC_OPTIONS = {
    Location_key.docker: ["http://elasticsearch:9200"],
    Location_key.local: [f"http://{get_docker_host()}:9201"],
    Location_key.override: [f"http://{EL_HOST_VAR}:{EL_PORT_VAR}"],
}

ELASTIC_SEARCH_HOSTS = ELASTIC_OPTIONS[get_database_key()]

ELASTIC_INDICES = dict(
    MEETBOUTEN='meetbouten', NAP='nap')

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

if TESTING:
    for k, v in ELASTIC_INDICES.items():
        ELASTIC_INDICES[k] += 'test'

BATCH_SETTINGS = dict(
    batch_size=100000
)

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

    'formatters': {
       'console': {
            # 'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'format': '%(levelname)s - %(name)s - %(message)s',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console',
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

REST_FRAMEWORK = dict(
    PAGE_SIZE=25,

    UNAUTHENTICATED_USER={},
    UNAUTHENTICATED_TOKEN={},

    MAX_PAGINATE_BY=100,
    DEFAULT_AUTHENTICATION_CLASSES=(
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    # DEFAULT_PAGINATION_CLASS='drf_hal_json.pagination.HalPageNumberPagination',
    # DEFAULT_PARSER_CLASSES=('drf_hal_json.parsers.JsonHalParser',),
    DEFAULT_RENDERER_CLASSES=(
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer'
    ),
    DEFAULT_FILTER_BACKENDS=(
        'rest_framework.filters.DjangoFilterBackend',
        # 'rest_framework.filters.OrderingFilter',

    ),
    COERCE_DECIMAL_TO_STRING=True,
)

# Security

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
# CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
X_FRAME_OPTIONS = 'DENY'

HEALTH_MODEL = 'nap.Peilmerk'

NAP_DECIMAL_PLACES = 4
NAP_MAX_DIGITS = 7  # if this is not enough, we have bigger problems

ZAKKING_DECIMAL_PLACES = 13
ZAKKING_MAX_DIGITS = 20

swag_path = 'acc.api.data.amsterdam.nl/meetbouten/docs'

if DEBUG:
    swag_path = '127.0.0.1:8000/meetbouten/docs'

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_path': '/',

    'enabled_methods': [
        'get',
    ],

    'api_key': '',

    'is_authenticated': False,
    'is_superuser': False,

    'unauthenticated_user': 'django.contrib.auth.models.AnonymousUser',
    'permission_denied_handler': None,
    'resource_access_handler': None,

    'protocol': 'https' if not DEBUG else '',
    'base_path': swag_path,

    'info': {
        'contact': 'atlas.basisinformatie@amsterdam.nl',
        'description': 'This is a meetbouten metingen api server. ',
        'license': 'Not known yet. Apache 2.0',
        'licenseUrl': 'http://www.apache.org/licenses/LICENSE-2.0.html',
        'termsOfServiceUrl': 'https://data.amsterdam.nl/terms/',
        'title': 'Meetbouten en metingen App',
    },
    'doc_expansion': 'list',
}
