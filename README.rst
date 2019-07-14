=================
Django Databrowse
=================

.. image:: https://travis-ci.org/Alir3z4/django-databrowse.png
   :alt: travis-cli tests status for django-databrowse
   :target: https://travis-ci.org/Alir3z4/django-databrowse

.. contents:: Table of contents

.. note::

    Extracted from `Django 1.4 since databrowse deprecation <https://docs.djangoproject.com/en/dev/releases/1.4/#django-contrib-databrowse>`_

------

Databrowse is a Django application that lets you browse your data.

As the Django admin dynamically creates an admin interface by introspecting
your models, Databrowse dynamically creates a rich, browsable Web site by
introspecting your models.

Installation
------------
``django-databrowse`` is available on pypi

http://pypi.python.org/pypi/django-databrowse

So easily install it by ``pip``
::
    
    $ pip install django-databrowse

Or by ``easy_install``
::
    
    $ easy_install django-databrowse

Another way is by cloning ``django-databrowse``'s `git repo <https://github.com/Alir3z4/django-databrowse>`_ ::
    
    $ git clone git://github.com/Alir3z4/django-databrowse.git

Then install it by running:
::
    
    $ python setup.py install


How to use Databrowse
---------------------

1. Point Django at the default Databrowse templates. There are two ways to
   do this:

   * Add ``'django_databrowse'`` to your `INSTALLED_APPS`
     setting. This will work if your `TEMPLATE_LOADERS` setting
     includes the ``app_directories`` template loader (which is the case by
     default). See the `template loader docs <https://docs.djangoproject.com/en/1.4/ref/templates/api/#template-loaders>`_ for more.

   * Otherwise, determine the full filesystem path to the
     `django_databrowse/templates` directory, and add that
     directory to your `TEMPLATE_DIRS <https://docs.djangoproject.com/en/1.4/ref/settings/#std:setting-TEMPLATE_DIRS>`_  setting.

2. Register a number of models with the Databrowse site::

       import django_databrowse
       from myapp.models import SomeModel, SomeOtherModel, YetAnotherModel

       django_databrowse.site.register(SomeModel)
       django_databrowse.site.register(SomeOtherModel, YetAnotherModel)

   Note that you should register the model *classes*, not instances.

   it is possible to register several models in the same
   call to `django_databrowse.site.register`.

   It doesn't matter where you put this, as long as it gets executed at some
   point. A good place for it is in your `URLconf file <https://docs.djangoproject.com/en/1.4/topics/http/urls/>`_ (``urls.py``).

3. Change your URLconf to import the `~django_databrowse` module::

       from django_databrowse

   ...and add the following line to your URLconf::

       (r'^django_databrowse/(.*)', django_databrowse.site.root),

   The prefix doesn't matter -- you can use ``databrowse/`` or ``db/`` or
   whatever you'd like.

4. Run the Django server and visit ``/databrowse/`` in your browser.

Requiring user login
---------------------

You can restrict access to logged-in users with only a few extra lines of
code. Simply add the following import to your URLconf::

    from django.contrib.auth.decorators import login_required

Then modify the `URLconf <https://docs.djangoproject.com/en/1.4/topics/http/urls/>`_ so that the
`django_databrowse.site.root` view is decorated with
`django.contrib.auth.decorators.login_required`::

    (r'^databrowse/(.*)', login_required(django_databrowse.site.root)),

If you haven't already added support for user logins to your `URLconf
<https://docs.djangoproject.com/en/1.4/topics/http/urls/>`_, as described in the `user authentication docs
<https://docs.djangoproject.com/en/1.4/ref/contrib/auth>`_, then you will need to do so now with the following
mapping::

    (r'^accounts/login/$', 'django.contrib.auth.views.login'),

The final step is to create the login form required by
`django.contrib.auth.views.login`. The
`user authentication docs <https://docs.djangoproject.com/en/1.4/ref/contrib/auth>`_ provide full details and a
sample template that can be used for this purpose.


Tests
-------------

``django-databrowse`` has been tested Django 1.6 and later. To run the the tests:

::
   
   $ python run_tests.py

It's also available on travis-ci:

https://travis-ci.org/Alir3z4/django-databrowse/


Translations
------------

Currently ``English`` is only available language that is being packaged. If you would like to contribute
in localization you can find ``django-databrowse`` project on Transifex as well:
https://www.transifex.com/projects/p/django-databrowse/

**Translation Status on Transifex**

.. image:: https://www.transifex.com/projects/p/django-databrowse/resource/django_databrowse/chart/image_png
   :alt: django-databrowse translation status on transifex
   :target: https://www.transifex.com/projects/p/django-databrowse/
   

Releasing
----------

* To make a release, first update the changelog with all the changes in the new release.
* Tag the git repository with the release version.
* Upload to PyPI.
* Update https://github.com/Alir3z4/django-databrowse/releases.
