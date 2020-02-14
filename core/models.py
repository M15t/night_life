# -*- coding: utf-8 -*-

import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _


FSHARE_CHOICE = 'FSHARE'
SOURCE_CHOICES = (
    (FSHARE_CHOICE, ('Fshare')),
)


class Video(models.Model):
    fs_url = models.CharField(max_length=100, blank=True, null=True)

    file_code = models.CharField(max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_url = models.TextField(blank=True, null=True)
    file_size = models.CharField(max_length=20, blank=True, null=True)
    file_type = models.CharField(max_length=30, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_current_time():
        now = datetime.datetime.now()
        return now.strftime('%m%d%y%I%M%S%f')

    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)


class FSConfig(models.Model):
    app_key = models.CharField(max_length=100, blank=True, null=True)

    token = models.CharField(max_length=100, blank=True, null=True)
    cookie = models.CharField(max_length=50, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super(FSConfig, self).save(*args, **kwargs)
