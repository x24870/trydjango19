from urllib.parse import quote_plus
from django import template

register = template.Library()

@register.filter
def urltify(value):
    return quote_plus(value)