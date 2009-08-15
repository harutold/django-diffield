# -*- coding: utf-8 -*-
from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe

from diffield.utils import diff_to_lists
from diffield.models import Diff

register = template.Library()
    
class DiffToHtmlNode(Node):
    def __init__(self, source, dest):
        self.source = template.Variable(source)
        self.dest = template.Variable(dest)

    def render(self, context):
        source = self.source.resolve(context)
        dest = self.dest.resolve(context)
        return _diff_to_html(source, dest)
        
class ObjectDiffToHtmlNode(Node):
    def __init__(self, object, rev1, rev2):
        self.object = template.Variable(object)
        self.rev1 = template.Variable(rev1)
        self.rev2 = template.Variable(rev2)

    def render(self, context):
        object = self.object.resolve(context)
        rev1 = self.rev1.resolve(context)
        rev2 = self.rev2.resolve(context)
        rev1, rev2 = min([rev1, rev2]), max([rev1, rev2])
        
        qs = Diff.objects.get_for_object(object)
        
        return _diff_to_html(qs.get(pk=rev1), qs.get(pk=rev2))
        
        

TAGS = {'-': 'del', '+': 'add', ' ': 'span'}
def _htmlize(diffstr):
    tag = TAGS[diffstr[0]]
    return "<td><%s>%s<%s></td>" % (tag, escape(diffstr[2:]), tag)
def _diff_to_html(source, dest):
    return mark_safe(u'<tr>' +    \
                [_htmlize(pair[0]) + htmlize(pair[1])
                    for pair in zip(diff_to_lists(source, dest))].join(u'</tr><tr>') \
            + u'</tr>')

def string_diff(parser, token):
    '''
    Outputs diff between two strings into a 2-column table (without <table> tags).
    Uses <del>, <add>, <span> tags in the cells
    
    usage:
    
    {% string_diff src dst %}
    '''
    tokens = token.contents.split()
    if len(tokens) != 3:
        raise TemplateSyntaxError(u"'%r' tag requires 2 arguments." % tokens[0])
    return DiffToHtmlNode(tokens[1], tokens[2])

def object_diff(parser, token):
    '''
    Same as string_diff but outputs diff between two revisions of given object
    
    usage:
    
    {% object_diff object rev1 rev2 %}
    '''
    tokens = token.contents.split()
    if len(tokens) != 4:
        raise TemplateSyntaxError(u"'%r' tag requires 3 arguments." % tokens[0])
    return DiffToHtmlNode(tokens[1], tokens[2], tokens[3])

register.tag(string_diff)
register.tag(object_diff)
