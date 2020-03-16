from django.contrib import admin
from .models import Entry, UserAuth


class EntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'temperature', 'owner', 'date_created')
    list_filter = ('date_created', 'owner')
    search_fields = ['owner__username', 'date_created']


admin.site.register(Entry, EntryAdmin)
admin.site.register(UserAuth)
