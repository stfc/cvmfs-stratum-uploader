# noinspection PyUnresolvedReferences
import os
from archer.settings.common import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG
# in memory doesn't work for nosetests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
        'TEST_NAME': ':memory:',
    },
}

# syncdb should be faster than using South migrations
SOUTH_TESTS_MIGRATE = False

INSTALLED_APPS = INSTALLED_APPS + (
    'django_nose',
    'django_extensions',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Use weak hashes to increase tests speed
PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.MD5PasswordHasher',
)

DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
