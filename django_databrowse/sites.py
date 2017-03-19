from django import http
try:
    from django.apps import apps
    get_model = apps.get_model
except ImportError:
    from django.db.models import get_model

from django.shortcuts import render
from django.template import RequestContext
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django_databrowse.datastructures import EasyModel


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class DatabrowsePlugin(object):
    def urls(self, plugin_name, easy_instance_field):
        """
        Given an EasyInstanceField object, returns a list of URLs for this
        plugin's views of this object. These URLs should be absolute.

        Returns None if the EasyInstanceField object doesn't get a
        list of plugin-specific URLs.
        """
        return None

    def model_index_html(self, request, model, site):
        """
        Returns a snippet of HTML to include on the model index page.
        """
        return ''

    def model_view(self, request, model_databrowse, url):
        """
        Handles main URL routing for a plugin's model-specific pages.
        """
        raise NotImplementedError


class ModelDatabrowse(object):
    plugins = {}

    def __init__(self, model, site):
        self.model = model
        self.site = site

    def root(self, request, url):
        """
        Handles main URL routing for the databrowse app.

        `url` is the remainder of the URL -- e.g. 'objects/3'.
        """
        # Delegate to the appropriate method, based on the URL.
        if url is None:
            return self.main_view(request)
        try:
            plugin_name, rest_of_url = url.split('/', 1)
        except ValueError:  # need more than 1 value to unpack
            plugin_name, rest_of_url = url, None
        try:
            plugin = self.plugins[plugin_name]
        except KeyError:
            raise http.Http404('A plugin with the requested name '
                               'does not exist.')
        return plugin.model_view(request, self, rest_of_url)

    def main_view(self, request):
        easy_model = EasyModel(self.site, self.model)
        html_snippets = mark_safe(
            u'\n'.join([p.model_index_html(
                request,
                self.model,
                self.site
            ) for p in self.plugins.values()])
        )
        obj_list = easy_model.objects()
        numitems = request.GET.get('items')
        items_per_page = [25, 50, 100]
        if numitems and numitems.isdigit() and int(numitems) > 0:
            paginator = Paginator(obj_list, numitems)
        else:
            # fall back to default
            paginator = Paginator(obj_list, items_per_page[0])

        page = request.GET.get('page')
        try:
            obj_list_page = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            obj_list_page = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page.
            obj_list_page = paginator.page(paginator.num_pages)
        return render(request,
            'databrowse/model_detail.html',
            {
                'model': easy_model,
                'root_url': self.site.root_url,
                'plugin_html': html_snippets,
                'object_list': obj_list_page,
                'items_per_page': items_per_page,
            }
        )


class DatabrowseSite(object):
    def __init__(self):
        self.registry = {}  # model_class -> databrowse_class
        self.root_url = None

    def register(self, *model_list, **options):
        """
        Registers the given model(s) with the given databrowse site.

        The model(s) should be Model classes, not instances.

        If a databrowse class isn't given, it will use DefaultModelDatabrowse
        (the default databrowse options).

        If a model is already registered, this will raise AlreadyRegistered.
        """
        databrowse_class = options.pop('databrowse_class',
                                       DefaultModelDatabrowse)
        for model in model_list:
            if model in self.registry:
                raise AlreadyRegistered('The model %s is already registered' %
                                        model.__name__)
            self.registry[model] = databrowse_class

    def unregister(self, *model_list):
        """
        Unregisters the given model(s).

        If a model isn't already registered, this will raise NotRegistered.
        """
        for model in model_list:
            if model not in self.registry:
                raise NotRegistered('The model %s is not registered' %
                                    model.__name__)
            del self.registry[model]

    def root(self, request, url):
        """
        Handles main URL routing for the databrowse app.

        `url` is the remainder of the URL -- e.g. 'comments/comment/'.
        """
        self.root_url = request.path[:len(request.path) - len(url)]
        url = url.rstrip('/')  # Trim trailing slash, if it exists.

        if url == '':
            return self.index(request)
        elif '/' in url:
            return self.model_page(request, *url.split('/', 2))

        raise http.Http404('The requested databrowse page does not exist.')

    def index(self, request):
        m_list = [EasyModel(self, m) for m in self.registry.keys()]
        return render(request,
            'databrowse/homepage.html',
            {'model_list': m_list, 'root_url': self.root_url},
        )

    def model_page(self, request, app_label, model_name, rest_of_url=None):
        """
        Handles the model-specific functionality of the databrowse site,
        delegating<to the appropriate ModelDatabrowse class.
        """
        try:
            model = get_model(app_label, model_name)
        except LookupError:
            model = None

        if model is None:
            raise http.Http404("App %r, model %r, not found." %
                               (app_label, model_name))
        try:
            databrowse_class = self.registry[model]
        except KeyError:
            raise http.Http404("This model exists but has not been registered "
                               "with databrowse.")
        return databrowse_class(model, self).root(request, rest_of_url)

site = DatabrowseSite()

from django_databrowse.plugins.calendars import CalendarPlugin
from django_databrowse.plugins.objects import ObjectDetailPlugin
from django_databrowse.plugins.fieldchoices import FieldChoicePlugin


class DefaultModelDatabrowse(ModelDatabrowse):
    plugins = {
        'objects': ObjectDetailPlugin(),
        'calendars': CalendarPlugin(),
        'fields': FieldChoicePlugin()
    }
