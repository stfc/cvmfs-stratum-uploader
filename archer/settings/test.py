# noinspection PyUnresolvedReferences
import os
from configurations import importer
importer.install()

from archer.settings.common import Common


class Test(Common):
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG

    # syncdb should be faster than using South migrations
    SOUTH_TESTS_MIGRATE = False

    INSTALLED_APPS = Common.INSTALLED_APPS + (
        'django_nose',
    )

    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
            'NAME': 'archer_test', # Or path to database file if using sqlite3.
            'USER': '', # Not used with sqlite3.
            'PASSWORD': '', # Not used with sqlite3.
            'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
            'PORT': '', # Set to empty string for default. Not used with sqlite3.
        }
    }

    # Use weak hashes to increase tests speed
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
