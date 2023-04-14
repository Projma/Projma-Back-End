from rest_framework import serializers
from board.models import Poll, PollAnswer


class PollKnownAnswerSerializer(serializers.ModelSerializer):
    voters = serializers.SerializerMethodField()
    class Meta:
        model = PollAnswer
        fields = ['id', 'text', 'poll', 'voters', 'count']
        read_only_fields = ['id', 'poll']

    def get_voters(self, answer: PollAnswer):
        return answer.voters.user.values('id', 'username')


class PollUnknownAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollAnswer
        fields = ['id', 'text', 'poll', 'count']
        read_only_fields = ['id', 'poll']


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'board', 'question', 'description', 'is_open', 'is_multianswer', 'is_known']
        read_only_fields = ['id']