# -*- coding: utf-8 -*-

import os.path
import pkg_resources
from importlib import import_module

from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import constants as messages
import tcms


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ You have to override the following settings in product.py


# Set to False for production
DEBUG = True


# Make this unique, and don't share it with anybody.
SECRET_KEY = '^8y!)$0t7yq2+65%&_#@i^_o)eb3^q--y_$e7a_=t$%$1i)zuv'  # nosec:B105


# Database settings
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('KIWI_DB_ENGINE', 'django.db.backends.mysql'),
        'NAME': os.environ.get('KIWI_DB_NAME', 'kiwi'),
        'USER': os.environ.get('KIWI_DB_USER', 'kiwi'),
        'PASSWORD': os.environ.get('KIWI_DB_PASSWORD', 'kiwi'),
        'HOST': os.environ.get('KIWI_DB_HOST', ''),
        'PORT': os.environ.get('KIWI_DB_PORT', ''),
        'OPTIONS': {},
    },
}

# handle MariaDB only options
if DATABASES['default']['ENGINE'].find('mysql') > -1:
    DATABASES['default']['OPTIONS'].update({
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        })


# Administrators error report email settings
ADMINS = [
    # ('Your Name', 'your_email@example.com'),
]


# Email settings
# DEFAULT_FROM_EMAIL must be defined if you want Kiwi TCMS to send emails.
# You also need to configure the email backend. For more information see:
# https://docs.djangoproject.com/en/2.0/topics/email/#quick-example
DEFAULT_FROM_EMAIL = 'kiwi@example.com'
EMAIL_SUBJECT_PREFIX = '[Kiwi-TCMS] '


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ You may want to override the following settings as well


# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.11/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']


# default group in which new users will be created
DEFAULT_GROUPS = ['Tester']


# When set to False site administrators will have to manually approve
# new users. You can combine this with tcms.signals.notify_admins() signal
# handler!
AUTO_APPROVE_NEW_USERS = True


# How often will session cookies expire? We set this to 24hrs by default.
# You may override based on your security policies
# https://docs.djangoproject.com/en/2.1/ref/settings/#session-cookie-age
SESSION_COOKIE_AGE = 86400


# Maximum upload file size, default set to 5MB.
FILE_UPLOAD_MAX_SIZE = 5242880


# Controls if django-attachments deletes files from disk
DELETE_ATTACHMENTS_FROM_DISK = True


# this is the main navigation menu
MENU_ITEMS = [
    (_('DASHBOARD'), reverse_lazy('core-views-index')),
    (_('TESTING'), [
        (_('New Test Plan'), reverse_lazy('plans-new')),
        ('-', '-'),
        (_('New Test Case'), reverse_lazy('testcases-new')),
    ]),
    (_('SEARCH'), [
        (_('Search Test Plans'), reverse_lazy('plans-search')),
        (_('Search Test Runs'), reverse_lazy('testruns-search')),
        (_('Search Test Cases'), reverse_lazy('testcases-search')),
    ]),
    (_('TELEMETRY'), [
        (_('Testing'), [
            (_('Breakdown'), reverse_lazy('testing-breakdown')),
            (_('Status matrix'), reverse_lazy('testing-status-matrix')),
            (_('Execution trends'), reverse_lazy('testing-execution-trends')),
        ]),
        ('More coming soon',
         'http://kiwitcms.org/blog/kiwi-tcms-team/2019/03/03/legacy-reports-become-telemetry/'),
    ]),
]

# last element is always TELEMETRY
for plugin in pkg_resources.iter_entry_points('kiwitcms.telemetry.plugins'):
    plugin_menu = import_module('%s.menu' % plugin.module_name)
    MENU_ITEMS[-1][1].extend(plugin_menu.MENU_ITEMS)

# append the ADMIN menu at the end
MENU_ITEMS.append(
    (_('ADMIN'), [
        (_('Users and groups'), '/admin/auth/'),
        ('-', '-'),
        (_('Everything else'), '/admin/'),
    ]),
)

# redefine the help menu in the navigation bar
HELP_MENU_ITEMS = [
    ('https://github.com/kiwitcms/Kiwi/issues/new', _('Report an Issue')),
    ('https://stackoverflow.com/questions/tagged/kiwi-tcms', _('Ask for help on StackOverflow')),
    ('http://kiwitcms.readthedocs.io/en/latest/tutorial.html', _('User Guide')),
    ('http://kiwitcms.readthedocs.io/en/latest/admin.html', _('Administration Guide')),
    ('http://kiwitcms.readthedocs.io/en/latest/api/index.html', _('API Help')),
]


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/Kiwi/static/'


# WARNING: Do not change this unless you know what you are doing !!!
# If you want to allow read-only access to anonymous users you can disable
# global_login_required.GlobalLoginRequiredMiddleware below!
MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'tcms.core.middleware.CsrfDisableMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'global_login_required.GlobalLoginRequiredMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
    'tcms.core.middleware.CheckSettingsMiddleware',
]


# You can also list additional views which will be available to
# anonymous users here. Take care to keep the default ones!
PUBLIC_VIEWS = [
    'modernrpc.views.RPCEntryPoint',
    'django.contrib.auth.views.LoginView',
    'django.contrib.auth.views.LogoutView',
    'django.contrib.auth.views.PasswordResetView',
    'django.contrib.auth.views.PasswordResetDoneView',
    'django.contrib.auth.views.PasswordResetConfirmView',
    'django.contrib.auth.views.PasswordResetCompleteView',
    'tcms.kiwi_auth.views.LoginViewWithCustomTemplate',
    'tcms.kiwi_auth.views.PasswordResetView',
    'tcms.kiwi_auth.views.register',
    'tcms.kiwi_auth.views.confirm',
    'tcms.core.views.navigation',
]


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# ~~ DANGER: Don't change the settings below!

SITE_ID = 1

KIWI_VERSION = tcms.__version__

MANAGERS = ADMINS

LOGIN_REDIRECT_URL = reverse_lazy('core-views-index')

# internal
TCMS_ROOT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..').replace('\\', '/'))

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# Language code for this installation. All choices can be found here:
# See https://code.djangoproject.com/ticket/29713
LANGUAGE_CODE = 'en-us'

LOCALE_PATHS = [
    os.path.join(TCMS_ROOT_PATH, 'locale'),
]

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = os.environ.get('KIWI_USE_TZ', 'False').lower() == 'true'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = os.environ.get('KIWI_TIME_ZONE', 'Etc/UTC')

# Absolute filesystem path to the directory that will hold user-uploaded files.
MEDIA_ROOT = '/Kiwi/uploads'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/uploads/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(TCMS_ROOT_PATH, 'static').replace('\\', '/'),
    os.path.join(TCMS_ROOT_PATH, 'node_modules').replace('\\', '/'),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(TCMS_ROOT_PATH, 'templates/').replace('\\', '/'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',

                'tcms.core.context_processors.request_contents_processor',
                'tcms.core.context_processors.settings_processor',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

ROOT_URLCONF = 'tcms.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'tcms.wsgi.application'

INSTALLED_APPS = [
    'vinaigrette',
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    'attachments',
    'django_comments',
    'modernrpc',
    'simple_history',

    'tcms.core',
    'tcms.kiwi_auth',
    'tcms.core.contrib.comments.apps.AppConfig',
    'tcms.core.contrib.linkreference',
    'tcms.management',
    'tcms.testcases.apps.AppConfig',
    'tcms.testplans.apps.AppConfig',
    'tcms.testruns.apps.AppConfig',
    'tcms.telemetry',
    'tcms.xmlrpc',

    'django_python3_ldap',
]

for plugin in pkg_resources.iter_entry_points('kiwitcms.telemetry.plugins'):
    INSTALLED_APPS.append(plugin.module_name)


SERIALIZATION_MODULES = {
    'json': 'tcms.core.serializer',
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

# Define the custom comment app
# http://docs.djangoproject.com/en/dev/ref/contrib/comments/custom/
COMMENTS_APP = 'tcms.core.contrib.comments'

# in alphabetic order
MODERNRPC_METHODS_MODULES = [
    'tcms.telemetry.api',
    'tcms.xmlrpc.api.attachment',
    'tcms.xmlrpc.api.auth',
    'tcms.xmlrpc.api.bug',
    'tcms.xmlrpc.api.build',
    'tcms.xmlrpc.api.bugsystem',
    'tcms.xmlrpc.api.category',
    'tcms.xmlrpc.api.classification',
    'tcms.xmlrpc.api.component',
    'tcms.xmlrpc.api.plantype',
    'tcms.xmlrpc.api.priority',
    'tcms.xmlrpc.api.product',
    'tcms.xmlrpc.api.tag',
    'tcms.xmlrpc.api.testcase',
    'tcms.xmlrpc.api.testexecution',
    'tcms.xmlrpc.api.testexecutionstatus',
    'tcms.xmlrpc.api.testcasestatus',
    'tcms.xmlrpc.api.testplan',
    'tcms.xmlrpc.api.testrun',
    'tcms.xmlrpc.api.user',
    'tcms.xmlrpc.api.version',
]

# Enable the administrator delete permission
# In another word it's set the admin to super user or not.
SET_ADMIN_AS_SUPERUSER = False

# Allows history_change_reason to be a TextField so we can
# support a changelog-like feature! DO NOT EDIT b/c migrations
# depend on this setting!
SIMPLE_HISTORY_HISTORY_CHANGE_REASON_USE_TEXT_FIELD = True

# Default page size when paginating queries
DEFAULT_PAGE_SIZE = 100

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s'
        },
        'xmlrpc_log': {
            'format': '[%(asctime)s] %(levelname)s XMLRPC %(process)d "%(message)s"'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'xmlrpc': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'xmlrpc_log',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'kiwi.xmlrpc': {
            'handlers': ['xmlrpc'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# override default message tags to match Patternfly class names
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

# A (workable) sample LDAP configuration.
# See https://github.com/etianen/django-python3-ldap and
# https://www.forumsys.com/tutorials/integration-how-to/ldap/online-ldap-test-server/
# for more details on how to customize your LDAP configuration.
# The URL of the LDAP server.
LDAP_AUTH_URL = "ldap://ldap.forumsys.com:389"

# Initiate TLS on connection.
LDAP_AUTH_USE_TLS = True

# The LDAP search base for looking up users.
LDAP_AUTH_SEARCH_BASE = "dc=example,dc=com"

# The LDAP class that represents a user.
LDAP_AUTH_OBJECT_CLASS = "inetOrgPerson"

# User model fields mapped to the LDAP
# attributes that represent them.
LDAP_AUTH_USER_FIELDS = {
    "username": "uid",
    "first_name": "givenName",
    "last_name": "sn",
    "email": "mail",
}

# A tuple of django model fields used to uniquely identify a user.
LDAP_AUTH_USER_LOOKUP_FIELDS = ("username",)

# Path to a callable that takes a dict of {model_field_name: value},
# returning a dict of clean model data.
# Use this to customize how data loaded from LDAP is saved to the User model.
LDAP_AUTH_CLEAN_USER_DATA = "django_python3_ldap.utils.clean_user_data"

# Path to a callable that takes a user model and a dict of {ldap_field_name: [value]},
# and saves any additional user relationships based on the LDAP data.
# Use this to customize how data loaded from LDAP is saved to User model relations.
# For customizing non-related User model fields, use LDAP_AUTH_CLEAN_USER_DATA.
LDAP_AUTH_SYNC_USER_RELATIONS = "django_python3_ldap.utils.sync_user_relations"

# Path to a callable that takes a dict of {ldap_field_name: value},
# returning a list of [ldap_search_filter]. The search filters will then be AND'd
# together when creating the final search filter.
LDAP_AUTH_FORMAT_SEARCH_FILTERS = "django_python3_ldap.utils.format_search_filters"

# Path to a callable that takes a dict of {model_field_name: value}, and returns
# a string of the username to bind to the LDAP server.
# Use this to support different types of LDAP server.
LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_openldap"

# Sets the login domain for Active Directory users.
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = None

# The LDAP username and password of a user for querying the LDAP database for user
# details. If None, then the authenticated user will be used for querying, and
# the `ldap_sync_users` command will perform an anonymous query.
# LDAP_AUTH_CONNECTION_USERNAME = "username"
# LDAP_AUTH_CONNECTION_PASSWORD = "password"

# Set connection/receive timeouts (in seconds) on the underlying `ldap3` library.
LDAP_AUTH_CONNECT_TIMEOUT = None
LDAP_AUTH_RECEIVE_TIMEOUT = None

# LDAP Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django_python3_ldap": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
    'django_python3_ldap.auth.LDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)
