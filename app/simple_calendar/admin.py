from django.contrib import admin
from .models import *


class SimpleCalendarAdmin(admin.ModelAdmin):
    model = SimpleCalendar
    fields = ['id', 'board']
    readonly_fields = ['id']


class EventAdmin(admin.ModelAdmin):
    model = Event
    fields = ['id', 'title', 'description', 'event_time', 'repeat_duration', 'event_color', 
              'event_type', 'custom_event_type', 'calendar']
    readonly_fields = ['id']


class MeetingAdmin(admin.ModelAdmin):
    model = Meeting
    fields = ['id', 'title', 'description', 'start', 'end', 'from_date', 'until_date', 'repeat',
              'link', 'status', 'created_at', 'updated_at', 'color', 'calendar', 'creator']
    readonly_fields = ['id', 'created_at', 'updated_at']


admin.site.register(SimpleCalendar, SimpleCalendarAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Meeting, MeetingAdmin)
