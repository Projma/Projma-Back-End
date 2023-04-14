from rest_framework import serializers
from board.models import Poll, PollAnswer


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'question', 'description', 'is_open', 'is_multianswer']
        read_only_fields = ['id']

