from django.db import models


class SomeModel(models.Model):
    some_field = models.CharField(max_length=50)

    def __unicode__(self):
        return self.some_field

    class Meta:
        db_table = "somemodel"


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

from datastructures import *
from sites import *
