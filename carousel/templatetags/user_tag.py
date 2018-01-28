    
##### Register own TAG for keys. Help to set up padding for threads
from django import template

register = template.Library()

@register.simple_tag

def user_tag(value):
    if value.lower() == "general feedback":
        return "badge-secondary"
    elif value.lower() == "mistake":
        return "badge-warning"
    elif value.lower() == "improvement":
        return "badge-primary"