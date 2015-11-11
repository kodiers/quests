"""
Django settings for quests project.

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
SECRET_KEY = '@l^@$lrfy!&ade_j9sskh^x*ds*h&wg@fs7@!=gbzy#=8^y&8&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tinymce',
    'web',
    'chat',
    'kronos',
    'pages',
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

ROOT_URLCONF = 'quests.urls'

WSGI_APPLICATION = 'quests.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

MEDIA_ROOT = (
    os.path.join(BASE_DIR, 'media')
)

MEDIA_URL = 'http://127.0.0.1:8000/media/'

# LOGIN URL
LOGIN_URL = 'login'

# EMAIL BACKEND (for developing process)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST_USER = 'test@test.ru'
FAIL_EMAIL_SILENTLY = False


# API KEY FOR TORNADO CHAT APPLICATION
API_KEY = '8W29kBOVkntM4+AqXJ/hyDVhHsmF02Qn'

# API ENDPOINT FOR TORNADO CHAT APPLICATION
API_URL = 'http://127.0.0.1:8000/messages/send_message_api/'


TEMPLATE_CONTEXT_PROCESSORS = (
    # Added request context_processor for forming URL in template (for search views)
    "django.core.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages"
)


# TINYMCE SETTINGS
TINYMCE_FILEBROWSER = True
TINYMCE_DEFAULT_CONFIG = {
    'plugins': "table,paste,searchreplace",
    'theme': "advanced",
    'mode': "textareas",
    'file_browser_callback': 'mce_filebrowser',
    'theme_advanced_buttons3_add': "tablecontrols",
    'table_styles': "Header 1=header1;Header 2=header2;Header 3=header3",
    'table_cell_styles': "Header 1=header1;Header 2=header2;Header 3=header3;Table Cell=tableCel1",
    'table_row_styles': "Header 1=header1;Header 2=header2;Header 3=header3;Table Row=tableRow1",
    'table_cell_limit': 100,
    'table_row_limit': 5,
    'table_col_limit': 5,
    'style_formats': [
        {'title': 'Bold text', 'inline': 'strong'},
        {'title': 'Red text', 'inline': 'span', 'styles' : {'color' : '#ff0000'}},
        {'title': 'Help', 'inline': 'strong', 'classes' : 'help'},
        {'title': 'Table styles'},
        {'title': 'Table row 1', 'selector': 'tr', 'classes': 'tablerow'}
    ],
    'width': '1140',
    'height': '800',
}