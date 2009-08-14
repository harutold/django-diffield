# -*- coding: utf-8 -*-

"""
Enforces default settings when the main settings module does not
contain the appropriate settings.
"""
from django.conf import settings

# Save full text in history, not diffs
SAVE_FULL_TEXT = getattr(settings, 'DIFF_SAVE_FULL_TEXT', False)

# Track users' contribution
TRACK_USERS = getattr(settings, 'DIFF_TRACK_USERS', True)

if TRACK_USERS:
    get_current_user = getattr(settings, 'DIFF_CURRENT_USER_FUNCTION', None)

    if get_current_user is None:
        from django_utils.middleware.threadlocals import get_current_user
        
    
