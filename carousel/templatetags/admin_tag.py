    
##### Register own TAG for keys. Help to set up padding for threads
from django import template

register = template.Library()

@register.simple_tag

def admin_tag(value):
    if value.lower() == "implemented":
        return "badge-success"
    elif value.lower() == "under consideration":
        return "badge-primary"
    elif value.lower() == "declined":
        return "badge-danger"