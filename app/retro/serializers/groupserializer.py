from django.db.models import Sum
from rest_framework import serializers
from retro.models import CardGroup


class CardGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardGroup
        fields = ['id', 'name', 'retro_session', 'is_discussed']


class DiscussCardGroupSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()
    class Meta:
        model = CardGroup
        fields = ['id', 'name', 'retro_session', 'is_discussed', 'votes']

    def get_votes(self, obj):
        total_votes = obj.retro_reactions.aggregate(vote_nums=Sum('count'))
        if total_votes['vote_nums']:
            return total_votes['vote_nums']
        return 0