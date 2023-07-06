from rest_framework import serializers
from retro.models import RetroSession, CardGroup, RetroCard, RetroReaction


class RetroSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroSession
        fields = ['id', 'board', 'attendees', 'admin']
        read_only_fields = ['id', 'board', 'admin']


class CardGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CardGroup
        fields = ['id', 'name', 'retro_session']
        read_only_fields = ['id']


class RetroCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroCard
        fields = ['id', 'card_group']
        read_only_fields = ['id']


class RetroReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroReaction
        fields = ['id', 'type', 'card_group']
        read_only_fields = ['id']