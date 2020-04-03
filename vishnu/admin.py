from datetime import datetime, timedelta

import pytz
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.html import format_html

from .models import Entry, UserAuth

PST = pytz.timezone('Singapore')


class DateIndexFilter(admin.SimpleListFilter):
    title = 'Date'
    parameter_name = 'date_index'

    def lookups(self, request, model_admin):
        date_index_param = max(int(request.GET.get('date_index', 0)), 0)
        return (
            (date_index_param+1, 'Previous'),
            (date_index_param-1, 'Next'),
            (0, 'Today')
        )

    def queryset(self, request, queryset):
        return queryset

    def choices(self, changelist):
        '''Override to remove the "All" Option
        Refer to https://stackoverflow.com/questions/53821727/django-admin-list-filter-remove-all-option
        '''
        yield {
            'selected': self.value() is None,
            'query_string': changelist.get_query_string({}, [self.parameter_name])
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup),
                'query_string': changelist.get_query_string({self.parameter_name: lookup}, []),
                'display': title,
            }


class Day:
    ''' Class implementation to allow column header to be dynamic
    Refer to https://stackoverflow.com/questions/19886218/django-admin-short-description-as-callable
    for additional information on how this was implemented
    '''

    def __init__(self, date):
        self.date = date

    def __call__(self, obj):
        return self.format_readings(self.get_readings(obj))

    def get_readings(self, obj):
        records = obj.records.filter(
            date_created__date=self.date).order_by('date_created')

        result = list()

        # if more than 1 record, we assume that there's AM and PM readings
        if records.count() > 1:
            for i in records:
                i.sgt_date_created = i.date_created.astimezone(PST)
            am_records = [i for i in records if i.sgt_date_created.hour < 12]
            pm_records = [i for i in records if i.sgt_date_created.hour > 12]
            am_temperature = am_records[len(am_records)-1].temperature if am_records else None
            pm_temperature = pm_records[len(pm_records)-1].temperature if pm_records else None
            result.append(am_temperature)
            result.append(pm_temperature)
        else:
            temperature = records.first().temperature if records.first() else None
            result.append(temperature)

        return result

    def format_readings(self, readings: list):
        formatted_readings = list()
        num_valid_readings = len([i for i in readings if i != None])
        for i in readings:
            if i == None:
                formatted_readings.append(format_html(''))
            elif i >= 38:
                formatted_readings.append(format_html('<mark style="color:red">{}</mark>', i))
            else:
                formatted_readings.append(format_html('{}', i))

        if num_valid_readings > 1:
            return format_html('<span>AM - ') + formatted_readings[0] + format_html('<br>') + format_html('PM - ') + formatted_readings[1] + format_html('</span>')

        else:
            return format_html('<span>') + formatted_readings[0] + format_html('</span>')

    @property
    def __name__(self):
        return self.date.strftime("%d %b")


class EntryAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['id', 'username'] + [f'day_{i}' for i in range(7)]
    list_filter = (DateIndexFilter, )
    list_display_links = None
    search_fields = ['id', 'username']
    filter_dates = [datetime.now(PST).date() - timedelta(days=i)
                    for i in range(6, -1, -1)]

    def get_queryset(self, request):
        date_index_param = max(int(request.GET.get('date_index', 0)), 0)
        self.update_filter_dates(date_index_param)
        qs = User.objects.all().order_by('id')
        return qs

    def changelist_view(self, request, extra_context=None):
        '''Override to change page title '''
        extra_context = {'title': 'Temperature Readings'}
        return super(EntryAdmin, self).changelist_view(request, extra_context=extra_context)

    def update_filter_dates(self, date_index):
        self.filter_dates = [
            datetime.now(PST).date() - timedelta(days=i+int(date_index)*7) for i in range(6, -1, -1)
        ]

    def get_property(self, index: int):
        if not hasattr(self, '__day'):
            self.__day = Day(self.filter_dates[index])
        return self.__day

    def username(self, obj): return obj.username
    username.short_description = 'Username'

    @property
    def day_6(self): return self.get_property(6)

    @property
    def day_5(self): return self.get_property(5)

    @property
    def day_4(self): return self.get_property(4)

    @property
    def day_3(self): return self.get_property(3)

    @property
    def day_2(self): return self.get_property(2)

    @property
    def day_1(self): return self.get_property(1)

    @property
    def day_0(self): return self.get_property(0)


admin.site.register(Entry, EntryAdmin)
admin.site.register(UserAuth)
