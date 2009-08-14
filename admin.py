from django.contrib import admin
from diffield.models import *

class DiffAdmin(admin.ModelAdmin):
    list_display = ('diff', 'text')

#admin.site.register(Diff, DiffAdmin)
