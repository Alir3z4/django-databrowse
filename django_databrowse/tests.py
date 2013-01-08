import django_databrowse
from django.db import models
from django.test import TestCase


class SomeModel(models.Model):
    some_field = models.CharField(max_length=50)

    def __unicode__(self):
        return self.some_field


class SomeOtherModel(models.Model):
    some_other_field = models.CharField(max_length=50)

    def __unicode__(self):
        return self.some_other_field


class YetAnotherModel(models.Model):
    yet_another_field = models.CharField(max_length=50)

    def __unicode__(self):
        return self.yet_another_field


class DatabrowseTests(TestCase):

    def test_databrowse_register_unregister(self):
        django_databrowse.site.register(SomeModel)
        self.assertTrue(SomeModel in django_databrowse.site.registry)
        django_databrowse.site.register(SomeOtherModel, YetAnotherModel)
        self.assertTrue(SomeOtherModel in django_databrowse.site.registry)
        self.assertTrue(YetAnotherModel in django_databrowse.site.registry)

        self.assertRaisesMessage(
            django_databrowse.sites.AlreadyRegistered,
            'The model SomeModel is already registered',
            django_databrowse.site.register, SomeModel, SomeOtherModel
        )

        django_databrowse.site.unregister(SomeOtherModel)
        self.assertFalse(SomeOtherModel in django_databrowse.site.registry)
        django_databrowse.site.unregister(SomeModel, YetAnotherModel)
        self.assertFalse(SomeModel in django_databrowse.site.registry)
        self.assertFalse(YetAnotherModel in django_databrowse.site.registry)

        self.assertRaisesMessage(
            django_databrowse.sites.NotRegistered,
            'The model SomeModel is not registered',
            django_databrowse.site.unregister, SomeModel, SomeOtherModel
        )

        self.assertRaisesMessage(
            django_databrowse.sites.AlreadyRegistered,
            'The model SomeModel is already registered',
            django_databrowse.site.register, SomeModel, SomeModel
        )

