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

    # Use weak hashes to increase tests speed
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    DEFAULT_FILE_STORAGE = 'inmemorystorage.InMemoryStorage'
