import os
import sys
import django
from django.conf import settings


DJANGO_VERSION = float('.'.join([str(i) for i in django.VERSION[0:2]]))
DIR_NAME = os.path.dirname(__file__)

settings.configure(
    DEBUG=True,
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
        }
    },
    INSTALLED_APPS=(
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.admin',
        'django_databrowse'
    ),
    MIDDLEWARE_CLASSES=[],
    ROOT_URLCONF='test_urls'
)

from django.test.simple import DjangoTestSuiteRunner

if DJANGO_VERSION >= 1.7:
    django.setup()

test_runner = DjangoTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(['django_databrowse', ])

if failures:
    sys.exit(failures)
