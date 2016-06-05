from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.contrib.auth.models import User, Group


@python_2_unicode_compatible
class Device(models.Model):
    name = models.CharField(max_length=50)
    latitude = models.FloatField()
    longitude = models.FloatField()
    distance = models.FloatField()
    users = models.ManyToManyField(User)

    def __str__(self):
        return '{}:({}, {})'.format(self.name, self.latitude, self.longitude)


@python_2_unicode_compatible
class Scenario(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(User)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    distance = models.FloatField(default=0.0)
    devices = models.ManyToManyField(Device)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ['distance']


@python_2_unicode_compatible
class Action(models.Model):
    name = models.CharField(max_length=30)
    scenario = models.ForeignKey(Scenario, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField()

    def __str__(self):
        return '{}'.format(self.name)
