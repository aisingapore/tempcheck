from datetime import datetime, timedelta

import pytz
from django.contrib import admin
from django.contrib.auth.models import User
from django.utils.html import format_html

from .models import Entry, UserAuth

PST = pytz.timezone('Singapore')


class EntryAdmin(admin.ModelAdmin):
    list_display = ['id', 'username'] + [f'day_{i}' for i in range(7)]
    list_display_links = None
    search_fields = ['id', 'username']
    filter_dates = [datetime.now(PST).date() - timedelta(days=i)
                    for i in range(6, -1, -1)]

    def get_queryset(self, request):
        print(request.GET)
        qs = User.objects.all().order_by('id')
        return qs

    def get_readings(self, obj, index: int):
        records = obj.records.filter(
            date_created__date=self.filter_dates[index]).order_by('date_created')

        result = list()

        # if more than 1 record, we assume that there's AM and PM readings
        if records.count() > 1:
            for i in records:
                i.sgt_date_created = i.date_created.astimezone(PST)
            am_records = [i for i in records if i.sgt_date_created.hour < 12]
            pm_records = [i for i in records if i.sgt_date_created.hour > 12]
            am_temperature = am_records[0].temperature if am_records else None
            pm_temperature = pm_records[0].temperature if pm_records else None
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
            elif i > 38:
                formatted_readings.append(format_html('<mark>{}</mark>', i))
            else:
                formatted_readings.append(format_html('{}', i))

        if num_valid_readings > 1:
            return format_html('<span>AM - ') + formatted_readings[0] + format_html('<br>') + format_html('PM - ') + formatted_readings[1] + format_html('</span>')

        else:
            return format_html('<span>') + formatted_readings[0] + format_html('</span>')

    def update_filter_dates(self, index):
        pass

    def username(self, obj): return obj.username
    username.short_description = 'Username'

    def day_6(self, obj):
        return self.format_readings(self.get_readings(obj, 6))
    day_6.short_description = filter_dates[6].strftime("%d %b")

    def day_5(self, obj):
        return self.format_readings(self.get_readings(obj, 5))
    day_5.short_description = filter_dates[5].strftime("%d %b")

    def day_4(self, obj):
        return self.format_readings(self.get_readings(obj, 4))
    day_4.short_description = filter_dates[4].strftime("%d %b")

    def day_3(self, obj):
        return self.format_readings(self.get_readings(obj, 3))
    day_3.short_description = filter_dates[3].strftime("%d %b")

    def day_2(self, obj):
        return self.format_readings(self.get_readings(obj, 2))
    day_2.short_description = filter_dates[2].strftime("%d %b")

    def day_1(self, obj):
        return self.format_readings(self.get_readings(obj, 1))
    day_1.short_description = filter_dates[1].strftime("%d %b")

    def day_0(self, obj):
        return self.format_readings(self.get_readings(obj, 0))
    day_0.short_description = filter_dates[0].strftime("%d %b")


admin.site.register(Entry, EntryAdmin)
admin.site.register(UserAuth)
