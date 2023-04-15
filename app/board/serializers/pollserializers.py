from rest_framework import serializers
from board.models import Poll, PollAnswer


class PollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['id', 'board', 'question', 'description', 'is_open', 'is_multianswer', 'is_known']
        read_only_fields = ['id']


class PollAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollAnswer
        fields = ['id', 'text', 'poll', 'voters', 'count']
        read_only_fields = ['id', 'voters', 'count']


class KnownAnswerSerializer(serializers.ModelSerializer):
    voters = serializers.SerializerMethodField()
    class Meta:
        model = PollAnswer
        fields = ['id', 'text', 'poll', 'voters', 'count']
        read_only_fields = ['id', 'voters', 'count', 'poll']

    def get_voters(self, ans):
        return ans.voters.values('user__pk', 'user__username')


class UnknownAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PollAnswer
        fields = ['id', 'text', 'poll', 'count']
        read_only_fields = ['id', 'count', 'poll']


class KnownPollSerializer(serializers.ModelSerializer):
    answers = KnownAnswerSerializer(many=True)
    class Meta:
        model = Poll
        fields = ['id', 'is_open', 'answers']


class UnknownPollSerializer(serializers.ModelSerializer):
    answers = UnknownAnswerSerializer(many=True)
    class Meta:
        model = Poll
        fields = ['id', 'is_open', 'answers']