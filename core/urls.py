#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.conf.urls import url

import views

urlpatterns = [
    url('^test/$', views.test, name='core_views_test'),

    url('^remove/(?P<video_id>.*)/$', views.remove, name='core_views_remove'),
    url('^list/$', views.list, name='core_views_list'),

    url('^(?P<code>.*)/$', views.index, name='core_views_play'),

    url('^$', views.index, name='core_views_index'),
]
