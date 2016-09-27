# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

from datapunt_generic.generic.database import get_docker_host

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIVA_DIR = os.path.abspath(os.path.join(BASE_DIR, './', 'diva'))

SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")

DEBUG = False

ALLOWED_HOSTS = ['*']

DATAPUNT_API_URL = os.getenv(
    # note the ending /
    'DATAPUNT_API_URL', 'https://api.datapunt.amsterdam.nl/')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.sites',

    # 'django_jenkins',
    #'django_extensions',

    'django.contrib.gis',
    'rest_framework',
    'rest_framework_gis',
    'rest_framework_swagger',

    # 'atlas',
    'geo_views',
    'atlas_api',
    'datasets.nap',
    'datasets.meetbouten',

    # legacy stuff? still used?
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
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'nap_meetbouten.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.getenv('DB_NAME', 'nap'),
        'USER': os.getenv('DB_USER', 'nap'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'insecure'),
        'HOST': os.getenv('DATABASE_PORT_5432_TCP_ADDR', get_docker_host()),
        'PORT': os.getenv('DATABASE_PORT_5432_TCP_PORT', '5401'),
    }
}


ELASTIC_SEARCH_HOSTS = [
    "http://{}:{}".format(
        os.getenv('ELASTIC_PORT_9200_TCP_ADDR', get_docker_host()),
        os.getenv('ELASTIC_PORT_9200_TCP_PORT', 9201))
]

ELASTIC_INDICES = dict(
    MEETBOUTEN='meetbouten', NAP='nap')

TESTING = len(sys.argv) > 1 and sys.argv[1] == 'test'

if TESTING:
    for k, v in ELASTIC_INDICES.items():
        ELASTIC_INDICES[k] = ELASTIC_INDICES[k] + 'test'

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

REST_FRAMEWORK = dict(
    PAGE_SIZE=25,
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
    DEFAULT_FILTER_BACKENDS=('rest_framework.filters.DjangoFilterBackend',),
    COERCE_DECIMAL_TO_STRING=False,
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

swag_path = 'api-acc.datapunt.amsterdam.nl/meetbouten/docs'

if DEBUG:
    swag_path = '127.0.0.1:8000/meetbouten/docs'

SWAGGER_SETTINGS = {
    'exclude_namespaces': [],
    'api_version': '0.1',
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
        'termsOfServiceUrl': 'https://atlas.amsterdam.nl/terms/',
        'title': 'Meetbouten en metingen App',
    },
    'doc_expansion': 'list',
}
