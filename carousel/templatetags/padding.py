    
##### Register own TAG for keys. Help to set up padding for threads
from django import template

register = template.Library()

@register.simple_tag

def padding(value, padding):
    return "padding-left: " + str(value * padding) + "%;"