#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

import views

urlpatterns = [
    url('^test/$', views.test, name='core_views_test'),

    url('^remove/(?P<video_id>.*)/$', views.remove, name='core_views_remove'),
    url('^list/$', views.list, name='core_views_list'),
    url('^get/$', views.get, name='core_views_get'),
    url('^play/(?P<code>.*)/$', views.play, name='core_views_play'),

    url('^$', views.index, name='core_views_index'),
]
