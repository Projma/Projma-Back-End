from rest_framework import serializers
from simple_calendar.models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'title', 'description', 'start', 'end', 'from_date', 'until_date', 'repeat',
                  'link', 'status', 'created_at', 'updated_at', 'creator', 'calendar', 'color']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at', 'creator', 'calendar', 'link']

    def validate(self, data):
        if data['start'] > data['end']:
            raise serializers.ValidationError("end time must be after start time")
        if data['from_date'] > data['until_date']:
            raise serializers.ValidationError("until_date must be after from_date")
        if data['repeat'] == 0 and data['from_date'] != data['until_date']:
            raise serializers.ValidationError("until_date and from_data must be equal for single meetings")

        return data
