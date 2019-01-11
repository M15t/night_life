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


class VideoFolder(models.Model):
    fs_url = models.CharField(max_length=100, blank=True, null=True)
    folder_name = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # do something here
        super(VideoFolder, self).save(*args, **kwargs)


class Video(models.Model):
    folder = models.ForeignKey(VideoFolder, blank=True, null=True)
    fs_url = models.CharField(max_length=100, blank=True, null=True)

    file_code = models.CharField(max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_url = models.CharField(max_length=500, blank=True, null=True)
    file_size = models.CharField(max_length=20, blank=True, null=True)
    file_type = models.CharField(max_length=10, blank=True, null=True)
    cover_img = models.ImageField(upload_to='cover', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_current_time():
        now = datetime.datetime.now()
        return now.strftime('%m%d%y%I%M%S%f')

    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)
