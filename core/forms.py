# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.forms import ModelForm
from django.forms.widgets import RadioSelect, TextInput, HiddenInput
from django.template import Template
from django.utils.text import slugify

from django.contrib.admin import widgets
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

import re


from models import *
from custom_widget import *
from form_utils import applyClassConfig2FormControl



