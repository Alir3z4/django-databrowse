from . import SomeModel, SomeInheritedModel

from django.test import TestCase
from django.db import models
import django_databrowse
from django_databrowse.datastructures import (EasyInstance, EasyModel,
                                              EasyQuerySet, EasyField,
                                              EasyChoice)

from django_databrowse.sites import DefaultModelDatabrowse


class EasyModelTest(TestCase):

    @classmethod
    def setUpClass(self):
        django_databrowse.site.register(SomeModel)

    @classmethod
    def tearDownClass(self):
        django_databrowse.site.unregister(SomeModel)

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

    def test_field(self):
        em = EasyModel(django_databrowse.site, SomeModel)
        self.assertIsInstance(em.field("some_field"), EasyField)
        self.assertEqual(em.field("hello"), None)

    def test_fields(self):
        em = EasyModel(django_databrowse.site, SomeModel)
        self.assertIsInstance(em.fields(), list)

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


class EasyFieldTest(TestCase):

    def test_repr(self):
        em = EasyModel(django_databrowse.site, SomeModel)
        field = EasyField(em, models.CharField(max_length=50, name="hello"))
        self.assertEqual(field.__repr__(), '<EasyField for SomeModel.hello>')

    def test_choices(self):
        em = EasyModel(django_databrowse.site, SomeModel)
        field = EasyField(
            em,
            models.CharField(max_length=2,
                             choices=(("a", "azerty"),("q","querty"))
                             )
            )
        self.assertEqual(len([f for f in field.choices()]), 2)

    def test_urls(self):
        em = EasyModel(django_databrowse.site, SomeModel)
        em.site.root_url = "root/"
        field = EasyField(
            em,
            models.CharField(max_length=2,
                             choices=(("a", "azerty"),("q","querty")),
                             name="hello"
                             )
            )
        self.assertEqual(field.url(),
                         u'root/django_databrowse/somemodel/hello/')

        em = EasyModel(django_databrowse.site, SomeInheritedModel)
        field = EasyField(em, models.ForeignKey(SomeModel))
        self.assertEqual(field.url(),
                         u'root/django_databrowse/someinheritedmodel/')


class EasyChoiceTest(TestCase):

    def test_repr(self):
        em = EasyModel(django_databrowse.site, SomeModel)
        field = models.CharField(max_length=2, name="Hello")
        value, label = "a", "azerty"
        ec = EasyChoice(em, field, value, label)
        self.assertEqual(ec.__repr__(), "<EasyChoice for SomeModel.Hello>")


class EasyInstanceTest(TestCase):

    def test_repr(self):
        instance = SomeModel.objects.create()
        ei = EasyInstance(EasyModel(django_databrowse.site,
                                    SomeModel), instance)
        self.assertEqual(ei.__repr__(), "<EasyInstance for SomeModel (1)>")
