# coding=utf-8
from django import template

register = template.Library()


@register.simple_tag
def call_with(obj, **kwargs):
    if 'method' not in kwargs:
        return False

    method = getattr(obj, kwargs['method'])
    del kwargs['method']
    return method(**kwargs)
