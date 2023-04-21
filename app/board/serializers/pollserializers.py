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
    is_user_voted = serializers.SerializerMethodField()
    class Meta:
        model = PollAnswer
        fields = ['id', 'text', 'poll', 'voters', 'count', 'is_user_voted']
        read_only_fields = ['id', 'voters', 'count', 'poll', 'is_user_voted']

    def get_voters(self, ans):
        return ans.voters.values('user__pk', 'user__username')

    def get_is_user_voted(self, ans):
        user = self.context.get('request').user.profile
        if user in ans.voters.all():
            return True
        return False


class UnknownAnswerSerializer(serializers.ModelSerializer):
    is_user_voted = serializers.SerializerMethodField()
    class Meta:
        model = PollAnswer
        fields = ['id', 'text', 'poll', 'count', 'is_user_voted']
        read_only_fields = ['id', 'count', 'poll', 'is_user_voted']

    def get_is_user_voted(self, ans):
        user = self.context.get('request').user.profile
        if user in ans.voters.all():
            return True
        return False


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