from django.conf.urls import patterns, include, url
import django_databrowse
urlpatterns = patterns('',
                       (r'^(.*)', django_databrowse.site.root)
                       )
