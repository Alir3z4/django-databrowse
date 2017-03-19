"""
These classes are light wrappers around Django's database API that provide
convenience functionality and permalink functions for the databrowse app.
"""

from django.db import models
from django.utils import formats
from django.utils.text import capfirst
from django.utils.encoding import smart_text, smart_text, iri_to_uri
from django.utils.safestring import mark_safe
from django.db.models.query import QuerySet
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import python_2_unicode_compatible


EMPTY_VALUE = '(None)'
DISPLAY_SIZE = 100


class EasyModel(object):
    def __init__(self, site, model):
        self.site = site
        self.model = model
        self.model_list = site.registry.keys()
        self.verbose_name = model._meta.verbose_name
        self.verbose_name_plural = model._meta.verbose_name_plural

    def __repr__(self):
        return '<EasyModel for %s>' % \
               smart_text(self.model._meta.object_name)

    def model_databrowse(self):
        "Returns the ModelDatabrowse class for this model."
        return self.site.registry[self.model]

    def url(self):
        return mark_safe('%s%s/%s/' % (self.site.root_url,
                                       self.model._meta.app_label,
                                       self.model._meta.model_name))

    def objects(self, **kwargs):
        return self.get_query_set().filter(**kwargs)

    def get_query_set(self):
        qs = self.model._default_manager.get_queryset()
        easy_qs = EasyQuerySet(model=qs.model, query=qs.query.clone(),
                                           using=qs._db, hints=qs._hints)
        easy_qs._easymodel = self
        return easy_qs

    def object_by_pk(self, pk):
        return EasyInstance(self, self.model._default_manager.get(pk=pk))

    def sample_objects(self):
        for obj in self.model._default_manager.all()[:3]:
            yield EasyInstance(self, obj)

    def field(self, name):
        try:
            f = self.model._meta.get_field(name)
        except models.FieldDoesNotExist:
            return None
        return EasyField(self, f)

    def fields(self):
        return [EasyField(self, f) for f in (self.model._meta.fields +
                                             self.model._meta.many_to_many)]


class EasyField(object):
    def __init__(self, easy_model, field):
        self.model, self.field = easy_model, field

    def __repr__(self):
        return smart_text(u'<EasyField for %s.%s>' %
                                        (self.model.model._meta.object_name,
                                         self.field.name))

    def choices(self):
        for value, label in self.field.choices:
            yield EasyChoice(self.model, self, value, label)

    def url(self):
        if self.field.choices:
            return mark_safe('%s%s/%s/%s/' %
                                    (self.model.site.root_url,
                                     self.model.model._meta.app_label,
                                     self.model.model._meta.model_name,
                                     self.field.name))
        elif self.field.rel:
            return mark_safe('%s%s/%s/' %
                                (self.model.site.root_url,
                                 self.model.model._meta.app_label,
                                 self.model.model._meta.model_name))

class EasyChoice(object):
    def __init__(self, easy_model, field, value, label):
        self.model, self.field = easy_model, field
        self.value, self.label = value, label

    def __repr__(self):
        return smart_text(u'<EasyChoice for %s.%s>' %
                                    (self.model.model._meta.object_name,
                                     self.field.name))

    def url(self):
        return mark_safe('%s%s/%s/%s/%s/' %
                             (self.model.site.root_url,
                              self.model.model._meta.app_label,
                              self.model.model._meta.model_name,
                              self.field.field.name,
                              iri_to_uri(self.value)))

@python_2_unicode_compatible
class EasyInstance(object):
    def __init__(self, easy_model, instance):
        self.model, self.instance = easy_model, instance

    def __repr__(self):
        return smart_text(u'<EasyInstance for %s (%s)>' %
                         (self.model.model._meta.object_name,
                          self.instance._get_pk_val()))

    def __str__(self):
        val = smart_text(self.instance)
        if len(val) > DISPLAY_SIZE:
            return val[:DISPLAY_SIZE] + u'...'
        return val

    def pk(self):
        return self.instance._get_pk_val()

    def url(self):
        return mark_safe('%s%s/%s/objects/%s/' %
                         (self.model.site.root_url,
                          self.model.model._meta.app_label,
                          self.model.model._meta.model_name,
                          iri_to_uri(self.pk())))

    def fields(self):
        """
        Generator that yields EasyInstanceFields for each field in this
        EasyInstance's model.
        """
        for f in self.model.model._meta.fields +\
                 self.model.model._meta.many_to_many:
            yield EasyInstanceField(self.model, self, f)

    def related_objects(self):
        """
        Generator that yields dictionaries of all models that have this
        EasyInstance's model as a ForeignKey or ManyToManyField, along with
        lists of related objects.
        """

        related_objects = [
            f for f in self.model.model._meta.get_fields()
            if (f.one_to_many or f.one_to_one)
            and f.auto_created and not f.concrete
        ]
        related_m2m = [
            f for f in self.model.model._meta.get_fields(include_hidden=True)
            if f.many_to_many and f.auto_created
        ]
        for rel_object in related_objects + related_m2m:
            if rel_object.model not in self.model.model_list:
                continue # Skip models that aren't in the model_list
            em = EasyModel(self.model.site, rel_object.model)
            try:
                rel_accessor = getattr(self.instance, rel_object.get_accessor_name())
            except ObjectDoesNotExist:
                continue
            if rel_object.field.rel.multiple:
                object_list = [EasyInstance(em, i) for i in rel_accessor.all()]
            else: # for one-to-one fields
                object_list = [EasyInstance(em, rel_accessor)]
            yield {
                'model': em,
                'related_field': rel_object.field.verbose_name,
                'object_list': object_list,
                }


class EasyInstanceField(object):
    def __init__(self, easy_model, instance, field):
        self.model, self.field, self.instance = easy_model, field, instance
        self.raw_value = getattr(instance.instance, field.name)

    def __repr__(self):
        return smart_text(u'<EasyInstanceField for %s.%s>' %
                         (self.model.model._meta.object_name,
                          self.field.name))

    def values(self):
        """
        Returns a list of values for this field for this instance. It's a list
        so we can accomodate many-to-many fields.
        """
        # This import is deliberately inside the function because it causes
        # some settings to be imported, and we don't want to do that at the
        # module level.
        if self.field.rel:
            if isinstance(self.field.rel, models.ManyToOneRel):
                objs = getattr(self.instance.instance, self.field.name)
            elif isinstance(self.field.rel,
                            models.ManyToManyRel): # ManyToManyRel
                return list(getattr(self.instance.instance,
                                    self.field.name).all())
        elif self.field.choices:
            objs = dict(self.field.choices).get(self.raw_value, EMPTY_VALUE)
        elif isinstance(self.field, models.DateField) or \
                                    isinstance(self.field, models.TimeField):
            if self.raw_value:
                if isinstance(self.field, models.DateTimeField):
                    objs = capfirst(formats.date_format(self.raw_value,
                                                        'DATETIME_FORMAT'))
                elif isinstance(self.field, models.TimeField):
                    objs = capfirst(formats.time_format(self.raw_value,
                                                        'TIME_FORMAT'))
                else:
                    objs = capfirst(formats.date_format(self.raw_value,
                                                        'DATE_FORMAT'))
            else:
                objs = EMPTY_VALUE
        elif isinstance(self.field, models.BooleanField) or \
                            isinstance(self.field, models.NullBooleanField):
            objs = {True: 'Yes', False: 'No', None: 'Unknown'}[self.raw_value]
        else:
            objs = self.raw_value
        return [objs]

    def urls(self):
        "Returns a list of (value, URL) tuples."
        # First, check the urls() method for each plugin.
        plugin_urls = []
        for plugin_name, plugin in \
                                self.model.model_databrowse().plugins.items():
            urls = plugin.urls(plugin_name, self)
            if urls is not None:
                #plugin_urls.append(urls)
                values = self.values()
                return zip(self.values(), urls)
        if self.field.rel:
            m = EasyModel(self.model.site, self.field.rel.to)
            if self.field.rel.to in self.model.model_list:
                lst = []
                for value in self.values():
                    if value is None:
                        continue
                    url = mark_safe('%s%s/%s/objects/%s/' %
                                            (self.model.site.root_url,
                                             m.model._meta.app_label,
                                             m.model._meta.model_name,
                                             iri_to_uri(value._get_pk_val())))
                    lst.append((smart_text(value), url))
            else:
                lst = [(value, None) for value in self.values()]
        elif self.field.choices:
            lst = []
            for value in self.values():
                url = mark_safe('%s%s/%s/fields/%s/%s/' %
                                        (self.model.site.root_url,
                                         self.model.model._meta.app_label,
                                         self.model.model._meta.model_name,
                                         self.field.name,
                                         iri_to_uri(self.raw_value)))
                lst.append((value, url))
        elif isinstance(self.field, models.URLField):
            val = self.values()[0]
            lst = [(val, iri_to_uri(val))]
        else:
            lst = [(self.values()[0], None)]
        return lst


class EasyQuerySet(QuerySet):
    """
    When creating (or cloning to) an `EasyQuerySet`, make sure to set the
    `_easymodel` variable to the related `EasyModel`.
    """
    def iterator(self, *args, **kwargs):
        for obj in super(EasyQuerySet, self).iterator(*args, **kwargs):
            yield EasyInstance(self._easymodel, obj)

    def _clone(self, *args, **kwargs):
        c = super(EasyQuerySet, self)._clone(*args, **kwargs)
        c._easymodel = self._easymodel
        return c
