from django.db.models import Sum
from rest_framework import serializers
from retro.models import CardGroup, RetroCard
from .cardserializer import SimpleRetroCardSerializer


class CardGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardGroup
        fields = ['id', 'name', 'retro_session', 'is_discussed']


class GroupsWithCardsSerializer(serializers.ModelSerializer):
    hide = serializers.BooleanField(default=False)
    cards = serializers.SerializerMethodField()

    class Meta:
        model = CardGroup
        fields = ['id', 'name', 'cards', 'hide']

    def get_cards(self, obj: CardGroup):
        cards = RetroCard.objects.filter(card_group=obj.pk)
        serializer = SimpleRetroCardSerializer(cards, many=True)
        return serializer.data


class DiscussCardGroupSerializer(serializers.ModelSerializer):
    votes = serializers.SerializerMethodField()
    cards = serializers.SerializerMethodField()

    class Meta:
        model = CardGroup
        fields = ['id', 'name', 'retro_session', 'is_discussed', 'votes', 'cards']

    def get_votes(self, obj):
        total_votes = obj.retro_reactions.aggregate(vote_nums=Sum('count'))
        if total_votes['vote_nums']:
            return total_votes['vote_nums']
        return 0

    def get_cards(self, obj: CardGroup):
        cards = RetroCard.objects.filter(card_group=obj.pk)
        serializer = SimpleRetroCardSerializer(cards, many=True)
        return serializer.data