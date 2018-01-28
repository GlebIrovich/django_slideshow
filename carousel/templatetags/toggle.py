    
##### Register own TAG for keys. Help to set up padding for threads
from django import template

register = template.Library()

@register.simple_tag

def toggle(value):
    if value.lower() == "block":
        return "collapse comment"
    else:
        return "show comments"
