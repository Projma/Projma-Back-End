from rest_framework import serializers
from simple_calendar.models import Meeting


class MeetingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meeting
        fields = ['id', 'title', 'description', 'start', 'end', 'from_date', 'until_date', 'repeat',
                  'link', 'status', 'created_at', 'updated_at', 'creator', 'calendar', 'color']
        read_only_fields = ['id', 'status', 'created_at', 'updated_at', 'creator', 'calendar', 'link']

    def validate(self, data):
        keys = data.keys()
        if not(('start' in keys and 'end' in keys) or ('start' not in keys and 'end' not in keys)):
            raise serializers.ValidationError("start and end time must be entered together")
        if not(('from_date' in keys and 'until_date' in keys and 'repeat' in keys) or\
                ('from_date' not in keys and 'until_date' not in keys and 'repeat' not in keys)):
            raise serializers.ValidationError("from_date and until_date and repeat must be entered together") 

        if 'start' in keys and data['start'] > data['end']:
            raise serializers.ValidationError("end time must be after start time")
        if 'from_date' in keys and data['from_date'] > data['until_date']:
            raise serializers.ValidationError("until_date must be after from_date")
        if 'repeat' in keys and data['repeat'] == 0 and data['from_date'] != data['until_date']:
            raise serializers.ValidationError("until_date and from_data must be equal for single meetings")

        return data
