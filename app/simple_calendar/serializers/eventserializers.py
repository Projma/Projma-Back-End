from rest_framework import serializers
from ..models import Event


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'event_time', 'repeat_duration', 
                  'event_color', 'event_type', 'custom_event_type', 'calendar']
        read_only_fields = ['id']