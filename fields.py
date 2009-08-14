# -*- coding: utf-8 -*-
"""
A custom Model DiffField with full history storage.
"""
from django.db.models import signals
from django.db.models.fields import TextField
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ImproperlyConfigured

from diffield import settings
from diffield.models import Diff
from diffield.utils import get_diff

class DiffField(TextField):
    """
    A "special" text field that saves full history of changes.
    """
    def __init__(self, *args, **kwargs):
        kwargs['default'] = kwargs.get('default', '')
        super(DiffField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(DiffField, self).contribute_to_class(cls, name)

        # Make this object the descriptor for field access.
        setattr(cls, self.name, self)
        
        try: cls._diffield_registered_on_this_class
        except AttributeError:
            cls._diffield_registered_on_this_class = True
        else: raise ImproperlyConfigured(u'Can not define two diffields in one class')

        # Save text back to the database post-save
        signals.post_save.connect(self._save, cls, True)

    def __set__(self, instance, value):
        """
        Set an object's text.
        """
        if instance is None:
            raise AttributeError(_('%s can only be set on instances.') % self.name)
        self._set_instance_text_cache(instance, value)


    def __get__(self, instance, default=''):
        if instance is None:
            return AttributeError(_('%s can only be get on instances.') % self.name)

        text = self._get_instance_text_cache(instance)
        if text is None:
            self._set_instance_text_cache(
                instance, self.value)
        return self._get_instance_text_cache(instance)
        
        
    def _save(self, **kwargs): #signal, sender, instance):
        """
        Save diff to the database
        """
        instance = kwargs['instance']
        text = self._get_instance_text_cache(instance)
        dic = self.__dict__
        if text != self.value:
            if settings.SAVE_FULL_TEXT:
                diff = text
            else:
                diff = get_diff(self.value, text)
            Diff(object=instance, diff=diff).save()
        self.value = text

    def _get_instance_text_cache(self, instance):
        """
        Helper: get an instance's text cache.
        """
        return getattr(instance, '_%s_cache' % self.attname, None)

    def _set_instance_text_cache(self, instance, value):
        """
        Helper: set an instance's text cache.
        """
        # Пока костылями, потом надо переделать
        if self._get_instance_text_cache(instance) is None:
            self.value = value
        setattr(instance, '_%s_cache' % self.attname, value)

    def get_internal_type(self):
        return 'TextField'
