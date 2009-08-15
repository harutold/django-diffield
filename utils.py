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

def _fill_lists(source_list, dest_list):
    # Need to be improved
    plm = len(source_list) - len(dest_list)
    if plm > 0:
        dest_list += [None] * plm
    elif plm < 0:
        source_list += [None] * (-plm)

def diff_to_lists(source, dest):
    '''
    Sorts diff into two columns
    '''
    last = ''
    last_not_changed = None
    source_list, dest_list = [], []
    
    for diffline in ndiff(source.splitlines(1), dest.splitlines(1)):
        if char == ' ':
            if last in '+-':
                _fill_lists(source_list, dest_list)
                
                source_list.append(diffline)
                dest_list.append(diffline)
                last_not_changed = None
            else:
                last_not_changed = diffline
        elif char == '-':
            source_list.append(diffline)
        elif char == '+':
            dest_list.append(diffline)
        elif char == '?':
            char = last
        else:
            raise AttributeError(u'Not correct diff in input!')
        last = char
        
    _fill_lists(source_list, dest_list)
    return (source_list, dest_list)

