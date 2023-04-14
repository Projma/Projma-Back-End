from rest_framework import serializers
from board.models import Poll, PollAnswer


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'question', 'description', 'is_open', 'is_multianswer']
        read_only_fields = ['id']

class PollKnownAnswerSerializer(serializers.ModelSerializer):
    voters = serializers.SerializerMethodField()
    class Meta:
        model = PollAnswer
        fields = ['id', 'text', 'poll', 'voters', 'count']
        read_only_fields = ['id', 'poll']

    def get_voters(self, answer: PollAnswer):
        return answer.voters.values('id', 'username')