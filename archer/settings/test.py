# noinspection PyUnresolvedReferences
from common import Common


class Test(Common):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    SOUTH_TESTS_MIGRATE = True

    INSTALLED_APPS = Common.INSTALLED_APPS + (
        'django_nose',
    )

    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'archer_dev', # Or path to database file if using sqlite3.
            'TEST_NAME': 'archer_test',
            # The following settings are not used with sqlite3:
            'USER': 'django',
            'PASSWORD': '234',
            'HOST': 'localhost', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
            'PORT': '', # Set to empty string for default.
        }
    }
