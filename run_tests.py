import os
import sys
from django.conf import settings
from django.conf.urls import patterns, include, url

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

    ROOT_URLCONF='test_urls'
)



from django.test.simple import DjangoTestSuiteRunner
test_runner = DjangoTestSuiteRunner(verbosity=1)
failures = test_runner.run_tests(['django_databrowse', ])

if failures:
    sys.exit(failures)
