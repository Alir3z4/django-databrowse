from django.test import TestCase
import django_databrowse
from . import SomeModel, SomeOtherModel, YetAnotherModel
from django.test import Client
from django_databrowse.datastructures import EasyModel


class DatabrowseTests(TestCase):

    @classmethod
    def tearDownClass(self):
        django_databrowse.site.unregister(SomeModel)

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


class DatabrowseTestsClient(TestCase):
    """
    Test the behavior of databrowse with a Client
    """
    @classmethod
    def tearDownClass(self):
        django_databrowse.site.unregister(SomeModel)

    def test_urls(self):
        django_databrowse.site.register(SomeModel)
        response = Client().get('')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(
            response.context['model_list'][0],
            EasyModel)

        response = Client().get('/django_databrowse/somemodel/')
        self.assertEqual(response.status_code, 200)

        response = Client().get('/django_databrowse/doesnotexistmodel/')
        self.assertEqual(response.status_code, 404)
        response = Client().get('/django_databrowse/something/somemodel/')
        self.assertEqual(response.status_code, 404)
        response = Client().get(
            '/django_databrowse/somemodel/fields/some_field/')
        self.assertEqual(response.status_code, 200)
        response = Client().get(
            '/django_databrowse/someothermodel/')
        self.assertEqual(response.status_code, 404)
