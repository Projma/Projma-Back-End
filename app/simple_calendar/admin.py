from django.contrib import admin
from .models import *

# Register your models here.
class SimpleCalendarAdmin(admin.ModelAdmin):
    model = SimpleCalendar
    fields = ['id', 'board']

class EventAdmin(admin.ModelAdmin):
    model = Event
    fields = ['title', 'description', 'event_time', 'repeat_duration', 'event_color', 
              'event_type', 'custom_event_type', 'calendar']


admin.site.register(SimpleCalendar, SimpleCalendarAdmin)
admin.site.register(Event, EventAdmin)