# -*- coding: utf-8 -*-
from django import template

register = template.Library()


@register.inclusion_tag('tags/getlink.html', takes_context=True)
def getlink(context):
    request = context['request']

    return {
        'request': request,
    }
