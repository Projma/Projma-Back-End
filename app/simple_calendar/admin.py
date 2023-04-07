from django.contrib import admin
from .models import *

# Register your models here.
class SimpleCalendarAdmin(admin.ModelAdmin):
    model = SimpleCalendar
    fields = ['id', 'board']
    readonly_fields = ['id']

class EventAdmin(admin.ModelAdmin):
    model = Event
    fields = ['id', 'title', 'description', 'event_time', 'repeat_duration', 'event_color', 
              'event_type', 'custom_event_type', 'calendar']
    readonly_fields = ['id']


admin.site.register(SimpleCalendar, SimpleCalendarAdmin)
admin.site.register(Event, EventAdmin)