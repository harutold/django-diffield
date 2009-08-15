DiffField
============

DiffField is django model field that stores self change history in database. 
DiffField is ancestor of models.TextField, stores data in Diff model.
Stored data is link to the object, author of the change and change in own 
internal diff format (truncated Python's difflib.ndiff format).

Note! Changes doesn't take an effect when using update method to modify this field!
It's not good idea! This problem should be fixed.

Usage
-----

#### settings.py
    MIDDLEWARE_CLASSES = (
        ... # Not required, see below
        'django_utils.middleware.threadlocals.ThreadLocals',
    )
    
    INSTALLED_APPS = (
        .....
        'diffield',
        .....
    )
    
    # Save full text in history, not diffs (in every diff)
    DIFF_SAVE_FULL_TEXT = False
    
    # Enable periodic text caching in database (every N revisions)
    DIFF_CACHE_TEXT = True
    
    # Save full text every SAVE_TEXT_CACHE_PERIOD times (the period of caching)
    DIFF_SAVE_TEXT_CACHE_PERIOD = 50
    
    # Track users' contribution (save diffs' authors)
    DIFF_TRACK_USERS = True

    # Some function returning auth.models.User object
    # Must be set if ThreadLocals is not used and DIFF_TRACK_USERS is True
    DIFF_CURRENT_USER_FUNCTION = some_function

#### appname.models.py file
Field contributes to a class as TextField. Usage with null=True is not tested yet.

    class MyModel(models.Model):
        title = DiffField(u'title')
    
#### getting text of some revision
    from diffield.models import Diff
    Diff.objects.get(**kwargs).text
