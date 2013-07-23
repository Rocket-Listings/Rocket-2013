import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

def specval(specs, arg):
    """Returns the spec value associated with the id"""
    spec = specs.get(arg, None)
    if spec:
        return spec.value
    else:
        return ""

register.filter('specval', specval)