from django.db.models import QuerySet
from rest_framework import serializers
from board.models import Poll, PollAnswer
from accounts.models import Profile

class PollSerializer(serializers.ModelSerializer):
    is_creator = serializers.SerializerMethodField()
    class Meta:
        model = Poll
        fields = ['id', 'board', 'creator', 'question', 'description', 'is_open', 'is_multianswer', 'is_known', 'is_creator']
        read_only_fields = ['id']

    def get_is_creator(self, poll):
        user = self.context.get('request').user.profile
        if poll.creator == user:
            return True
        return False


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
    all_voters_count = serializers.SerializerMethodField()
    class Meta:
        model = Poll
        fields = ['id', 'is_open', 'answers', 'all_voters_count']

    def get_all_voters_count(self, poll: Poll):
        answers = poll.answers.all()
        voters = None
        for ans in answers:
            if voters:
                voters = voters.union(ans.voters.all())
            else:
                voters = ans.voters.all()
        return len(voters)


class UnknownPollSerializer(serializers.ModelSerializer):
    answers = UnknownAnswerSerializer(many=True)
    all_voters_count = serializers.SerializerMethodField()
    class Meta:
        model = Poll
        fields = ['id', 'is_open', 'answers', 'all_voters_count']

    def get_all_voters_count(self, poll: Poll):
        answers = poll.answers.all()
        voters = None
        for ans in answers:
            if voters:
                voters = voters.union(ans.voters.all())
            else:
                voters = ans.voters.all()
        return len(voters)