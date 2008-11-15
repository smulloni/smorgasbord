from __future__ import absolute_import

from django.conf import settings

from mako.exceptions import MakoException
from mako.template import Template
from mako.lookup import TemplateLookup

from ..contextutil import context_to_dict

def _get_start_and_end(source, lineno, pos):
    start=0
    for n, line in enumerate(source.splitlines()):
        if n==lineno:
            start+=pos
            break
        else:
            start+=len(line)-1
    return start, start

class MakoExceptionWrapper(Exception):
    def __init__(self, exc, origin):
        self._exc=exc
        self._origin=origin
        self.args=self._exc.args

    def __getattr__(self, name):
        return getattr(self._exc, name)

    @property
    def source(self):
        return (self._origin,
                _get_start_and_end(self._exc.source,
                                   self._exc.lineno,
                                   self._exc.pos))



class MakoTemplate(object):
    def __init__(self, template_obj, origin=None):
        self.template_obj=template_obj
        self.origin=origin

    def render(self, context):
        return self.template_obj.render_unicode(**context_to_dict(context))

def get_template_from_string(source, origin=None, name=None):
    lookup=TemplateLookup(directories=settings.MAKO_TEMPLATE_DIRS)
    # other lookup settings from configuration ...
    # TBD
    try:
        real_template=Template(source, lookup=lookup)
        return MakoTemplate(real_template)
    except MakoException, me:
        if hasattr(me, 'source'):
            raise(MakoExceptionWrapper(me, origin))
        else:
            raise me


    
