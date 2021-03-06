from django import template
from django.core import urlresolvers
  
register = template.Library()
 
@register.simple_tag(takes_context=True)
def active(context, *args, **kwargs):
    word = kwargs.pop('value', 'active')
    matches = any(map(lambda url: current_url_equals(context, url, **kwargs), args))
    return word if matches else ''
 
def current_url_equals(context, url_name, **kwargs):
    resolved = False
    try:
        resolved = urlresolvers.resolve(context.get('request').path)
    except:
        pass
    matches = resolved and resolved.url_name == url_name
    if matches and kwargs:
        for key in kwargs:
            kwarg = kwargs.get(key)
            resolved_kwarg = resolved.kwargs.get(key)
            if not resolved_kwarg or kwarg != resolved_kwarg:
                return False
    return matches