from rest_framework import serializers
from retro.models import RetroReaction



class RetroReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RetroReaction
        fields = ['id', 'card_group', 'reactor', 'count']
        read_only_fields = ['id']