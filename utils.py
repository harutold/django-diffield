# -*- coding: utf-8 -*-

from difflib import ndiff

def get_diff(source, dest):
    """
    Gets the diff to save into the database
    """
    diff = []
    # Removing overweight info
    for diffline in ndiff(source.splitlines(1), dest.splitlines(1)):
        char = diffline[0]
        if char in [' ', '-']:
            diff.append(char + '\n')
        elif char == '+':
            diff.append(diffline)
        elif char == '?':
            pass
        else:
            raise AttributeError(u'Not correct diff in input!')
    return ''.join(diff)
    
def load_diff(source, diff):
    dest = source.splitlines(1)
    i = 0
    for diffline in diff.splitlines(1):
        char = diffline[0]
        if char == ' ':
            i += 1
        elif char == '-':
            dest.pop(i)
        elif char == '+':
            dest.insert(i, diffline[2:])
            i += 1
        elif not char:
            pass
        else:
            raise AttributeError(u'Not correct diff in input!')
    return ''.join(dest)
    
    

def get_queryset_and_model(queryset_or_model):
    """
    Given a ``QuerySet`` or a ``Model``, returns a two-tuple of
    (queryset, model).

    If a ``Model`` is given, the ``QuerySet`` returned will be created
    using its default manager.
    """
    try:
        return queryset_or_model, queryset_or_model.model
    except AttributeError:
        return queryset_or_model._default_manager.all(), queryset_or_model

