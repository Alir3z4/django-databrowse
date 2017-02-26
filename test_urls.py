from django.conf.urls import url
import django_databrowse

urlpatterns = [
    url(r'^(.*)', django_databrowse.site.root),
]
