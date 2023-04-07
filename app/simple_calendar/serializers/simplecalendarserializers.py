from rest_framework import serializers
from simple_calendar.models import SimpleCalendar

class SimpleCalendarSerializer(serializers.ModelSerializer):
    class Meta:
        model = SimpleCalendar
        fields = ['id', 'board']
        read_only_fields = ['id']