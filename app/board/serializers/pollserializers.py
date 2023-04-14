from rest_framework import serializers
from board.models import Poll, PollAnswer


class PollSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()
    class Meta:
        model = Poll
        fields = ['id', 'question', 'description', 'is_open', 'is_multianswer', 'answers']
        read_only_fields = ['id', 'answers']

    def get_answers(self, poll):
        if poll.is_known:
            return PollKnownAnswerSerializer(many=True)
        return PollUnknownAnswerSerializer(many=True)


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