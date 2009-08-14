# -*- coding: utf-8 -*-

"""
Models and managers for diff calculations.
"""
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.db import connection, models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from diffield import settings
from diffield.utils import load_diff
############
# Managers #
############

class DiffManager(models.Manager):

    def get_for_object(self, obj):
        """
        Create a queryset matching all tags associated with the given
        object.
        """
        ctype = ContentType.objects.get_for_model(obj)
        return self.filter(content_type__pk=ctype.pk,
                           object_id=obj.pk)

##########
# Models #
##########

class Diff(models.Model):
    """
    A diff between two editions
    """
    diff = models.TextField(_('diff'))
    # TODO: May be, include caching text every N diffs
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'))
    object_id    = models.PositiveIntegerField(_('object id'), db_index=True)
    object       = generic.GenericForeignKey('content_type', 'object_id')
    user         = models.ForeignKey(User, verbose_name=_('diff author'), blank=True, null=True)

    objects = DiffManager()

    @property
    def diff_history(self):
        '''
        Always return a list (not QuerySet) of older diffs including self
        '''
        if not hasattr(self, '_diff_history'):
            self._diff_history = Diff.objects.get_for_object(self.object).filter(pk__lte=self.pk).order_by('pk')
            self._diff_history = list(self._diff_history)
        return self._diff_history

    @property
    def text(self):
        '''
        Text in version of this diff
        '''
        if settings.SAVE_FULL_TEXT:
            return self.diff
        else:
            if not hasattr(self, '_txt'):
                diffs = self.diff_history
                if len(diffs) == 1:
                    txt = ''
                else:
                    diffs[-2]._diff_history = diffs[:-1]
                    txt = diffs[-2].text
                # Recursively counting diffs. May be it's not a good idea
                self._txt = load_diff(txt, self.diff)
            return self._txt
        
    def save(self, *args, **kwargs):
        if settings.TRACK_USERS and not self.user_id:
            self.user = settings.get_current_user()
        super(Diff, self).save(*args, **kwargs)
            
    class Meta:
        ordering = ('id',)
        verbose_name = _('diff')
        verbose_name_plural = _('diffs')

    def __unicode__(self):
        return self.text
