from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

import re

trac_ticket_regex = re.compile(r'(#(\d+))');

@register.filter
@stringfilter
def trac_parse(value, trac_url):
    if trac_url:
        result = trac_ticket_regex.sub(r'<a href="%sticket/\2">\1</a>' % trac_url, value)
    else:
        result = value
    return result