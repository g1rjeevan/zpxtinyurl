# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TinyURL(models.Model):
    givenurl = models.URLField(max_length=200)
    biturl = models.URLField(max_length=200)
    hitcount = models.PositiveIntegerField(null=True)