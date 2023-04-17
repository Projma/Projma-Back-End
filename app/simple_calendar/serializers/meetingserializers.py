from rest_framework import serializers
from simple_calendar.models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'title', 'description', 'start', 'end', 'from_data', 'until_date', 'repeat', 
                  'link', 'status', 'created_at', 'updated_at', 'creator', 'calendar', 'color']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at', 'creator', 'calendar']