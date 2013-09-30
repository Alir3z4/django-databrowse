from django.db import models
from django.test import TestCase

import django_databrowse
from django_databrowse.datastructures import (EasyInstance, EasyModel,
                                              EasyQuerySet)
from django_databrowse.sites import DefaultModelDatabrowse


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


class SomeInheritedModel(SomeModel):
    special = models.CharField(max_length=30)


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

    def test_model_inheritance(self):
        django_databrowse.site.register(SomeInheritedModel)
        child = SomeInheritedModel.objects.create(some_field='hello',
                                                  special='world')
        ei = EasyInstance(EasyModel(django_databrowse.site,
                                    SomeModel), child)
        ei_child = EasyInstance(EasyModel(django_databrowse.site,
                                          SomeInheritedModel), child)
        self.assertEqual(
            ei.related_objects().next()['object_list'][0].instance,
            ei_child.instance)

    def test_model_inheritance_no_child(self):
        instance = SomeModel.objects.create(some_field='hello')
        ei = EasyInstance(EasyModel(django_databrowse.site, SomeModel),
                          instance)
        self.assertEqual(list(ei.related_objects()), [])


class EasyModelTest(TestCase):

    def test_repr(self):
        em = EasyModel(django_databrowse.site, SomeModel)
        self.assertEqual(em.__repr__(), "<EasyModel for SomeModel>")

    def test_model_databrowse(self):
        em = EasyModel(django_databrowse.site, SomeModel)
        self.assertEqual(em.model_databrowse(), DefaultModelDatabrowse)

    def test_url(self):
        em = EasyModel(django_databrowse.site, SomeModel)
        em.site.root_url = "root/"
        self.assertEqual(em.url(), u'root/django_databrowse/somemodel/')

    def test_manager(self):
        em = EasyModel(django_databrowse.site, SomeModel)
        self.assertIsInstance(em.objects(), EasyQuerySet)
