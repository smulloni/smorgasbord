from __future__ import absolute_import

from django.conf import settings

import jinja2

from ..contextutil import context_to_dict

class Jinja2Template(object):

    def __init__(self, template_obj):
        self.template_obj=template_obj

    def render(self, context):
        return self.template_obj.render(context_to_dict(context))

def get_template_from_string(source, origin=None, name=None):
    
    loader=jinja2.FileSystemLoader(settings.JINJA2_TEMPLATE_DIRS)
    # other settings from configuration ...
    # TBD
    environment=jinja2.Environment(loader=loader)
    template=environment.from_string(source)
    template.name=name
    return Jinja2Template(template)
