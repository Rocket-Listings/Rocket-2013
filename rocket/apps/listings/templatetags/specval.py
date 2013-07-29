import re
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()

def specval(specs, key):
    """Returns the spec value associated with the id"""
    if specs and key in specs:
        spec = specs.get(key, None)
        if spec:
            return spec.value
    return ""

register.filter('specval', specval)