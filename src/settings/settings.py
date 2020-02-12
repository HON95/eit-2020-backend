import os
import sys

# Settings directory
SETTINGS_DIR = os.path.dirname(os.path.abspath(__file__))
# Root directory
BASE_DIR = os.path.normpath(os.path.join(SETTINGS_DIR, '..', '..'))
# Settings package
SETTINGS_PACKAGE = 'settings'

SECRET_KEY = ''
DEBUG = False
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # App
    'api.apps.ApiConfig',
    'web.apps.WebConfig',
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

ROOT_URLCONF = 'urls'

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

WSGI_APPLICATION = 'wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

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

# i18n
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '[%(asctime)s] [%(levelname)s] %(message)s',
        },
    },
    'handlers': {
        'error_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'log/error.log',
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['error_file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Static files
# Absolute path to the directory static files should be collected to.
STATIC_ROOT = 'static/'
# URL prefix for static files.
STATIC_URL = '/static/'
# URL prefix for admin static files.
ADMIN_MEDIA_PREFIX = '/static/admin/'
# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'res'),
]
# List of finder classes that know how to find static files in various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Security
CSRF_COOKIE_PATH = '/'
CSRF_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

# Read version from file
VERSION = '0'
version_file_path = os.path.join(BASE_DIR, 'VERSION')
if os.path.isfile(version_file_path):
    with open(version_file_path, 'r') as version_file:
        content = version_file.read()
    content = content.strip()
    if (content):
        VERSION = content

# Load local settings
# Remember to keep 'local' last, so it can override any setting.
for settings_module in ['local']:
    full_settings_module = '{0}.{1}'.format(SETTINGS_PACKAGE, settings_module)
    sys.stdout.write(u'Loading settings from "{0}".\n'.format(full_settings_module))
    if not os.path.exists(os.path.join(SETTINGS_DIR, settings_module + '.py')):
        sys.stderr.write(u'Could not find settings module "{0}".\n'.format(settings_module))
        if settings_module == 'local':
            sys.stderr.write('You need to add the settings file "src/settings/local.py".\n')
        sys.exit(1)
    try:
        exec(u'from {0} import *'.format(full_settings_module))  # noqa: S102
    except ImportError as e:
        print(u'Could not import settings for "{0}": {1}'.format(full_settings_module, str(e)))  # noqa: T001
        sys.exit(1)