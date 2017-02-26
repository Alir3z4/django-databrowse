import os
import sys
import django
from django.conf import settings
from django.core.management import call_command


def main():
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
        TEST_RUNNER='django.test.runner.DiscoverRunner',
        MIDDLEWARE_CLASSES=[],
        ROOT_URLCONF='test_urls'
    )

    django.setup()

    call_command('test')


if __name__ == '__main__':
    main()
